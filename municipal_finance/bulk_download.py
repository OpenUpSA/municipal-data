import xlsxwriter
import os
import hashlib
import json
import csv
from datetime import datetime
from .views import get_cube

from sqlalchemy import select
from babbage.query import Cuts, Fields

from django.core.files.storage import default_storage
from django.conf import settings

# Stream data from the DB in chunks of this size
stream_chunk_size = 10000

# Limit the size of the blocks used when hashing a finished file
hash_block_size = 8 * 1024 * 1024

# Map cube names to call the get_cube function
cubes_map = {
    "financial_position_facts_v2": "financial_position_v2",
    "aged_debtor_facts_v2": "aged_debtor_v2",
    "aged_creditor_facts_v2": "aged_creditor_v2",
    "capital_facts_v2": "capital_v2",
    "cflow_facts_v2": "cflow_v2",
    "grant_facts_v2": "grants_v2",
    "incexp_facts_v2": "incexp_v2",
    "audit_opinion_facts": "audit_opinions",
    "municipal_staff_contacts": "municipalities",
    "repairs_maintenance_facts_v2": "repmaint_v2",
    "uifwexp_facts_v1": "uifwexp",
}

# Controls which cubes to split by year
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

# Split cubes that also get a single file covering every year
all_years_cubes = [
    "aged_debtor_facts_v2",
    "capital_facts_v2",
    "cflow_facts_v2",
    "financial_position_facts_v2",
    "grant_facts_v2",
    "incexp_facts_v2",
]

# Disable cubes with years that have more than more million rows per year
disable_xlsx = [
    "cflow_facts_v2",
    "incexp_facts",
    "incexp_facts_v2",
]

xlsx_max_rows = 1000000
all_years = "All"
metadata_index = "index.json"


def generate_download(**kwargs):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    cube_model = kwargs["cube_model"]
    cube_name = cube_model._meta.db_table
    file_names = {}

    if cube_name in split_cubes:
        year_list = (
            cube_model.objects.all().distinct().values_list("financial_year", flat=True)
        )

        if cube_name in all_years_cubes:
            file_names[all_years] = cube_to_csv(cube_model, timestamp)[all_years]

        if cube_name in disable_xlsx:
            file_names.update(split_cube_to_csv(cube_model, timestamp, year_list))
        else:
            # xlsx_files = split_dump_to_xlsx(
            #    field_names, cube_model, timestamp, year_list
            # )
            csv_files = split_cube_to_csv(cube_model, timestamp, year_list)
            for year in csv_files.keys():
                file_names[year] = csv_files[year]  # + xlsx_files[year]
    else:
        # xlsx_files = dump_cube_to_xlsx(queryset, field_names, cube_model, timestamp)
        csv_files = cube_to_csv(cube_model, timestamp)
        file_names[all_years] = csv_files[all_years]  # + xlsx_files[all_years]

    save_metadata(file_names, cube_name, timestamp)


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


def stream_cube_facts(cube, cuts=None):
    """Stream every fact of a cube to disk without loading it to memory."""

    query = select(columns=None).select_from(cube.fact_table)
    bindings = []
    _, query, bindings = Cuts(cube).apply(query, bindings, cuts)
    query = cube.restrict_joins(query, bindings)
    field_refs, query, bindings = Fields(cube).apply(query, bindings, None)
    query = cube.restrict_joins(query, bindings)

    def rows():
        connection = cube.engine.connect()
        try:
            result = connection.execution_options(
                stream_results=True
            ).execute(query)
            while True:
                batch = result.fetchmany(stream_chunk_size)
                if not batch:
                    break
                for row in batch:
                    yield dict(row.items())
        finally:
            connection.close()

    return field_refs, rows()


def cube_to_csv(cube_model, timestamp):
    file_name = f"{cube_model._meta.db_table}_{timestamp}.csv"
    cube = get_cube(cubes_map[cube_model._meta.db_table])
    field_refs, rows = stream_cube_facts(cube)
    headers = field_labels(cube, field_refs)
    write_to_csv(headers, rows, cube_model, file_name)
    return {all_years: [file_name]}


def split_cube_to_csv(cube_model, timestamp, year_list):
    cube = get_cube(cubes_map[cube_model._meta.db_table])
    files = {}

    for year in year_list:
        file_name = f"{cube_model._meta.db_table}_{year}__{timestamp}.csv"
        field_refs, rows = stream_cube_facts(
            cube, cuts=f"financial_year_end.year:{year}"
        )
        headers = field_labels(cube, field_refs)
        files[year] = [file_name]
        write_to_csv(headers, rows, cube_model, file_name)
    return files


def field_labels(cube, field_names):
    """Map babbage field refs (e.g. ``l120_amount``, ``demarcation.code``) to the
    human-readable labels shown on the data explorer tables, falling back to the
    ref itself when no label is defined in the cube model."""
    model = cube.model.to_dict()
    measures = model.get("measures", {})
    dimensions = model.get("dimensions", {})

    headers = []
    for ref in field_names:
        label = None
        if ref in measures:
            label = measures[ref].get("label")
        elif "." in ref:
            dim_name, attr_name = ref.split(".", 1)
            attribute = (
                dimensions.get(dim_name, {}).get("attributes", {}).get(attr_name, {})
            )
            label = attribute.get("label")
        headers.append(label or ref)
    return headers


def write_to_csv(headers, rows, cube_model, file_name):
    file_path = f"{settings.BULK_DOWNLOAD_DIR}/{cube_model._meta.db_table}/{file_name}"
    with default_storage.open(file_path, "wb") as file:
        writer = csv.writer(file)

        writer.writerow(headers)
        for fact in rows:
            writer.writerow(fact.values())


def save_metadata(file_names, cube_name, timestamp):
    file_metadata = {}
    for file_year in file_names:
        file_metadata[file_year] = []
        for name in file_names[file_year]:
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            size = 0
            with default_storage.open(
                f"{settings.BULK_DOWNLOAD_DIR}/{cube_name}/{name}", "rb"
            ) as f:
                for block in iter(lambda: f.read(hash_block_size), b""):
                    md5.update(block)
                    sha1.update(block)
                    size += len(block)
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
