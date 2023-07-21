import xlsxwriter
import sys
import hashlib
import json
import csv
from datetime import datetime

from django.core.files.storage import default_storage
from django.db import transaction


import logging

logger = logging.Logger(__name__)

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

storage_dir = "bulk_downloads"


@transaction.atomic
def generate_download(**kwargs):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    cube_model = kwargs["cube_model"]
    cube_name = kwargs["cube_model"]._meta.db_table
    file_names = {}

    queryset = cube_model.objects.all().defer("id")
    field_names = [field.name for field in cube_model._meta.fields]

    if "id" in field_names:
        field_names.remove("id")

    # Pull data from relevent cube
    if cube_name in split_cubes:
        if cube_name in disable_xlsx:
            file_names = split_dump_to_csv(queryset, field_names, cube_model, timestamp)
        else:
            xlsx_files = split_dump_to_xlsx(
                queryset, field_names, cube_model, timestamp
            )
            csv_files = split_dump_to_csv(queryset, field_names, cube_model, timestamp)
            for year in csv_files.keys():
                file_names[year] = xlsx_files[year] + csv_files[year]
    else:
        xlsx_files = dump_cube_to_xlsx(queryset, field_names, cube_model, timestamp)
        csv_files = dump_cube_to_csv(queryset, field_names, cube_model, timestamp)
        file_names["All"] = xlsx_files["All"] + csv_files["All"]

    # Draw metadata for this dump
    file_metadata = {}
    for file_year in file_names:
        file_metadata[file_year] = []
        for name in file_names[file_year]:
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            with default_storage.open(f"{storage_dir}/{cube_name}/{name}", "rb") as f:
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
                }
            )

    metadata = {
        cube_name: {
            "last_updated": timestamp,
            "files": file_metadata,
        }
    }

    with default_storage.open(f"{storage_dir}/{cube_name}/index.json", "w") as file:
        json.dump(metadata, file)

    # Aggregate all metadata
    aggregate_index = f"{storage_dir}/index.json"
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
    max_rows = 1000000
    file_name = f"{cube_model._meta.db_table}_{timestamp}.xlsx"
    f = default_storage.open(
        f"{storage_dir}/{cube_model._meta.db_table}/{file_name}", "wb"
    )
    workbook = xlsxwriter.Workbook(f, {"constant_memory": True})
    worksheet = workbook.add_worksheet()

    # Generalise header for different cube columns
    for col, header in enumerate(field_names):
        worksheet.write(0, col, header)

    row = 1
    for item in queryset:
        col = 0
        for field in cube_model._meta.get_fields():
            # Handle related fields
            if field.concrete:
                if field.is_relation:
                    if field.many_to_many or field.one_to_many:
                        value = ", ".join(
                            str(obj) for obj in getattr(item, field.name).all()
                        )
                else:
                    value = getattr(item, field.name)
                worksheet.write(row, col, value)
                col += 1
        row += 1

        if row > max_rows:
            worksheet = workbook.add_worksheet()
            row = 0

    workbook.close()
    f.close()
    return {"All": [file_name]}


def split_dump_to_xlsx(queryset, field_names, cube_model, timestamp):
    current_year = 0
    max_rows = 1000000
    files = []
    files_dev = {}

    for item in queryset:
        col = 0

        if item.financial_year != current_year:
            try:
                workbook.close()
                f.close()
            except:
                pass

            row = 1
            current_year = item.financial_year
            file_name = f"{cube_model._meta.db_table}_{current_year}__{timestamp}.xlsx"
            files.append(f"{file_name}")
            files_dev[current_year] = [file_name]
            f = default_storage.open(
                f"{storage_dir}/{cube_model._meta.db_table}/{file_name}", "wb"
            )
            workbook = xlsxwriter.Workbook(f, {"constant_memory": True})
            worksheet = workbook.add_worksheet()

            # Generalise header for different cube columns
            for col, header in enumerate(field_names):
                worksheet.write(0, col, header)
        else:
            for field in cube_model._meta.get_fields():
                # Handle related fields
                if field.concrete:
                    if field.is_relation:
                        if field.many_to_many or field.one_to_many:
                            value = ", ".join(
                                str(obj) for obj in getattr(item, field.name).all()
                            )
                    else:
                        value = getattr(item, field.name)
                    worksheet.write(row, col, value)
                    col += 1
            row += 1

        if row > max_rows:
            worksheet = workbook.add_worksheet()
            row = 0

    workbook.close()
    f.close()
    return files_dev


def dump_cube_to_csv(queryset, field_names, cube_model, timestamp):
    file_name = f"{cube_model._meta.db_table}_{timestamp}.csv"

    f = default_storage.open(
        f"{storage_dir}/{cube_model._meta.db_table}/{file_name}", "wb"
    )
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    for item in queryset:
        row = {field: getattr(item, field) for field in field_names}
        writer.writerow(row)

    f.close()
    return {"All": [file_name]}


def split_dump_to_csv(queryset, field_names, cube_model, timestamp):
    current_year = 0
    files = []
    files_dev = {}

    for item in queryset:
        if item.financial_year != current_year:
            try:
                f.close()
            except:
                pass

            current_year = item.financial_year
            file_name = f"{cube_model._meta.db_table}_{current_year}__{timestamp}.csv"
            files.append(f"{file_name}")
            files_dev[current_year] = [file_name]
            f = default_storage.open(
                f"{storage_dir}/{cube_model._meta.db_table}/{file_name}", "wb"
            )

            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
        else:
            row = {field: getattr(item, field) for field in field_names}
            writer.writerow(row)

    f.close()
    return files_dev
