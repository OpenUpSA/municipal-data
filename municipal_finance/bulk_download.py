import xlsxwriter
import sys
import hashlib
import json
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

storage_dir = "bulk_downloads"


@transaction.atomic
def generate_download(**kwargs):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    cube_model = kwargs["cube_model"]
    cube_name = kwargs["cube_model"]._meta.db_table

    # Pull data from relevent cube
    if cube_name in split_cubes:
        file_names = split_dump_to_excel(cube_model, timestamp)
        # file_names = dump_cube_to_excel(cube_model, timestamp)
    else:
        file_names = dump_cube_to_excel(cube_model, timestamp)


    logger.warn(f"____________{file_names}")
    # Draw metadata for this dump
    file_metadata = []
    for name in file_names:
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        with default_storage.open(f"{storage_dir}/{cube_name}/{name}", "rb") as f:
            data = f.read()
            md5.update(data)
            sha1.update(data)
            size = sys.getsizeof(data)

        file_metadata.append(
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


def dump_cube_to_excel(cube_model, timestamp):
    queryset = cube_model.objects.all()
    max_rows = 1000000
    #file_name = f"{storage_dir}/{cube_model._meta.db_table}/{cube_model._meta.db_table}_{timestamp}.xlsx"
    file_name = f"{cube_model._meta.db_table}_{timestamp}.xlsx"
    file = default_storage.open(f"{storage_dir}/{cube_model._meta.db_table}/{file_name}", "wb")
    workbook = xlsxwriter.Workbook(file, {"constant_memory": True})
    worksheet = workbook.add_worksheet()

    # Generalise header for different cube columns
    headers = [field.verbose_name.title() for field in cube_model._meta.get_fields()]
    for col, header in enumerate(headers):
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
    file.close()
    return [file_name]


def split_dump_to_excel(cube_model, timestamp):
    queryset = cube_model.objects.all().order_by("financial_year")

    current_year = 0
    max_rows = 1000000
    files = []
    for item in queryset:
        col = 0

        if item.financial_year != current_year:
            try:
                workbook.close()
                file.close()
            except:
                pass

            row = 1
            current_year = item.financial_year
            #file_name = f"{storage_dir}/{cube_model._meta.db_table}/{cube_model._meta.db_table}_{current_year}__{timestamp}.xlsx"
            file_name = f"{cube_model._meta.db_table}_{current_year}__{timestamp}.xlsx"
            files.append(f"{file_name}")
            file = default_storage.open(f"{storage_dir}/{cube_model._meta.db_table}/{file_name}", "wb")
            workbook = xlsxwriter.Workbook(file, {"constant_memory": True})
            worksheet = workbook.add_worksheet()

            # Generalise header for different cube columns
            headers = [
                field.verbose_name.title() for field in cube_model._meta.get_fields()
            ]
            for col, header in enumerate(headers):
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
    file.close()
    return files
