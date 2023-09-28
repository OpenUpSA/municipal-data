import xlsxwriter
import sys
import os
import hashlib
import json
import csv
from datetime import datetime

from django.core.files.storage import default_storage
from django.db import transaction
from django.conf import settings


split_cubes = [
    "bsheet_facts",
    "financial_position_facts_v2",
    "aged_debtor_facts",
    "aged_debtor_facts_v2",
    "capital_facts",
    "capital_facts_v2",
    "cflow_facts",
    "cflow_facts_v2",
    "conditional_grant_facts",
    "grant_facts_v2",
    "incexp_facts",
    "incexp_facts_v2",
]

disable_xlsx = [
    "incexp_facts",
    "incexp_facts_v2",
]

xlsx_max_rows = 1000000
all_years = "All"
metadata_index = "index.json"


@transaction.atomic
def generate_download(**kwargs):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    cube_model = kwargs["cube_model"]
    cube_name = cube_model._meta.db_table
    file_names = {}

    queryset = cube_model.objects.all().defer("id")
    field_names = [field.name for field in cube_model._meta.fields]

    if "id" in field_names:
        field_names.remove("id")

    # Fetch data from relevent cube
    if cube_name in split_cubes:
        year_list = (
            cube_model.objects.all()
            .distinct()
            .values_list("financial_year", flat=True)
        )

        if cube_name in disable_xlsx:
            file_names = split_dump_to_csv(
                field_names, cube_model, timestamp, year_list
            )
        else:
            xlsx_files = split_dump_to_xlsx(
                field_names, cube_model, timestamp, year_list
            )
            csv_files = split_dump_to_csv(field_names, cube_model, timestamp, year_list)
            for year in csv_files.keys():
                file_names[year] = xlsx_files[year] + csv_files[year]
    else:
        xlsx_files = dump_cube_to_xlsx(queryset, field_names, cube_model, timestamp)
        csv_files = dump_cube_to_csv(queryset, field_names, cube_model, timestamp)
        file_names[all_years] = xlsx_files[all_years] + csv_files[all_years]

    # Draw metadata for this dump
    file_metadata = {}
    for file_year in file_names:
        file_metadata[file_year] = []
        for name in file_names[file_year]:
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            with default_storage.open(
                f"{settings.BULK_DOWNLOAD_DIR}/{cube_name}/{name}", "rb"
            ) as f:
                data = f.read()
                md5.update(data)
                sha1.update(data)
                size = sys.getsizeof(data)
            file_metadata[file_year].append(
                {
                    "file_name": name,
                    "md5": md5.hexdigest(),
                    "sha1": sha1.hexdigest(),
                    "file_size": size,
                    "format": os.path.splitext(name)[1][1:],
                }
            )

    metadata = {
        cube_name: {
            "last_updated": timestamp,
            "files": file_metadata,
        }
    }

    with default_storage.open(
        f"{settings.BULK_DOWNLOAD_DIR}/{cube_name}/{metadata_index}", "w"
    ) as file:
        json.dump(metadata, file)

    # Aggregate all metadata
    aggregate_index = f"{settings.BULK_DOWNLOAD_DIR}/{metadata_index}"
    if default_storage.exists(aggregate_index):
        with default_storage.open(aggregate_index, "r") as file:
            data = json.load(file)

        data[cube_name] = {
            "last_updated": timestamp,
            "files": file_metadata,
        }

        with default_storage.open(aggregate_index, "w") as file:
            json.dump(data, file)

    else:
        with default_storage.open(aggregate_index, "w") as file:
            json.dump(metadata, file)


def dump_cube_to_xlsx(queryset, field_names, cube_model, timestamp):
    file_name = f"{cube_model._meta.db_table}_{timestamp}.xlsx"
    f = default_storage.open(
        f"{settings.BULK_DOWNLOAD_DIR}/{cube_model._meta.db_table}/{file_name}", "wb"
    )
    workbook = xlsxwriter.Workbook(f, {"constant_memory": True})
    worksheet = workbook.add_worksheet()

    # Generalise header for different cube columns
    for col, header in enumerate(field_names):
        worksheet.write(0, col, header)

    row_num = 1
    for row in queryset:
        col_num = 0
        for field in field_names:
            value = getattr(row, field)
            worksheet.write(row_num, col_num, str(value))
            col_num += 1
        row_num += 1

        if row_num > xlsx_max_rows:
            worksheet = workbook.add_worksheet()
            row = 0

    workbook.close()
    f.close()
    return {all_years: [file_name]}


def split_dump_to_xlsx(field_names, cube_model, timestamp, year_list):
    files = {}

    for year in year_list:
        file_name = f"{cube_model._meta.db_table}_{year}__{timestamp}.xlsx"
        file_path = (
            f"{settings.BULK_DOWNLOAD_DIR}/{cube_model._meta.db_table}/{file_name}"
        )
        files[year] = [file_name]
        queryset_year = cube_model.objects.filter(financial_year=year).defer("id")
        total_rows = queryset_year.count()
        num_chunks = (total_rows // xlsx_max_rows) + 1

        with default_storage.open(file_path, "wb") as file:
            workbook = xlsxwriter.Workbook(file, {"constant_memory": True})
            worksheet = workbook.add_worksheet()

            for col_num, header in enumerate(field_names):
                worksheet.write(0, col_num, header)

            # Write data in chunks
            current_row = 1
            for chunk_number in range(num_chunks):
                start_row = chunk_number * xlsx_max_rows
                end_row = min((chunk_number + 1) * xlsx_max_rows, total_rows)
                chunk = queryset_year[start_row:end_row]

                for row_num, row in enumerate(chunk):
                    for col_num, field in enumerate(cube_model._meta.get_fields()):
                        if field.name != "id":
                            value = getattr(row, field.name)
                            worksheet.write(
                                current_row + row_num, col_num - 1, str(value)
                            )

                current_row += len(chunk)

            workbook.close()
    return files


def dump_cube_to_csv(queryset, field_names, cube_model, timestamp):
    file_name = f"{cube_model._meta.db_table}_{timestamp}.csv"

    f = default_storage.open(
        f"{settings.BULK_DOWNLOAD_DIR}/{cube_model._meta.db_table}/{file_name}", "wb"
    )
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    for item in queryset:
        row = {field: getattr(item, field) for field in field_names}
        writer.writerow(row)

    f.close()
    return {all_years: [file_name]}


def split_dump_to_csv(field_names, cube_model, timestamp, year_list):
    files = {}
    for year in year_list:
        queryset_new = cube_model.objects.filter(financial_year=year).defer("id")
        file_name = f"{cube_model._meta.db_table}_{year}__{timestamp}.csv"
        file_path = (
            f"{settings.BULK_DOWNLOAD_DIR}/{cube_model._meta.db_table}/{file_name}"
        )
        files[year] = [file_name]

        with default_storage.open(file_path, "wb") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for item in queryset_new:
                row = {field: getattr(item, field) for field in field_names}
                writer.writerow(row)
    return files
