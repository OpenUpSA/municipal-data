import xlsxwriter
import sys
import os
import hashlib
import json
import csv
from datetime import datetime

from django.core.files.storage import default_storage
from django.db.models import ForeignKey
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

# Disable cubes with years that have more than more million rows
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

    queryset = cube_model.objects.select_related().all().defer("id")
    field_names = [field.name for field in cube_model._meta.fields]

    if "id" in field_names:
        field_names.remove("id")

    # Fetch data from relevent cube
    if cube_name in split_cubes:
        year_list = (
            cube_model.objects.all().distinct().values_list("financial_year", flat=True)
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
    write_to_xlsx(field_names, queryset, cube_model, file_name)
    return {all_years: [file_name]}


def split_dump_to_xlsx(field_names, cube_model, timestamp, year_list):
    # Write each year to a separate file
    files = {}

    for year in year_list:
        file_name = f"{cube_model._meta.db_table}_{year}__{timestamp}.xlsx"
        files[year] = [file_name]
        queryset_year = cube_model.objects.filter(financial_year=year).defer("id")
        write_to_xlsx(field_names, queryset_year, cube_model, file_name)
    return files


def write_to_xlsx(field_names, queryset, cube_model, file_name):
    file_path = f"{settings.BULK_DOWNLOAD_DIR}/{cube_model._meta.db_table}/{file_name}"

    with default_storage.open(file_path, "wb") as file:
        workbook = xlsxwriter.Workbook(file)
        worksheet = workbook.add_worksheet()

        header_written = False

        row_num = 0
        for fact in queryset:
            fields = get_related_fields(fact)

            # Write the header row
            if not header_written:
                for col_num, field_name in enumerate(fields.keys()):
                    worksheet.write(row_num, col_num, field_name)
                header_written = True
                row_num += 1
            # Write the data rows
            for col_num, field_value in enumerate(fields.values()):
                worksheet.write(row_num, col_num, field_value)
            row_num += 1

        workbook.close()


def dump_cube_to_csv(queryset, field_names, cube_model, timestamp):
    file_name = f"{cube_model._meta.db_table}_{timestamp}.csv"
    write_to_csv(field_names, queryset, cube_model, file_name)
    return {all_years: [file_name]}


def split_dump_to_csv(field_names, cube_model, timestamp, year_list):
    # Write each year to a separate file
    files = {}
    for year in year_list:
        queryset = cube_model.objects.filter(financial_year=year).defer("id")
        file_name = f"{cube_model._meta.db_table}_{year}__{timestamp}.csv"
        files[year] = [file_name]
        write_to_csv(field_names, queryset, cube_model, file_name)
    return files


def write_to_csv(field_names, queryset, cube_model, file_name):
    file_path = f"{settings.BULK_DOWNLOAD_DIR}/{cube_model._meta.db_table}/{file_name}"
    with default_storage.open(file_path, "wb") as file:
        writer = csv.writer(file)

        header_written = False

        for fact in queryset:
            fields = get_related_fields(fact)

            if not header_written:
                writer.writerow(fields.keys())
                header_written = True

            writer.writerow(fields.values())


def get_related_fields(instance):
    fields = {}
    for field in instance._meta.get_fields():
        value = getattr(instance, field.name)
        if isinstance(field, ForeignKey):
            value = str(value) if value else None
        fields[field.name] = value
    return fields
