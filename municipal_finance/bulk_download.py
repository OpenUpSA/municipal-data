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
    "repairs_maintenance_facts_v2": "repmaint_v2",
    "uifwexp_facts_v1": "uifwexp",
}

# Cubes that are not published, so no bulk download is generated for them even
# though their data is still updated through the admin.
excluded_cubes = [
    "municipal_staff_contacts",
]

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

    if cube_name in excluded_cubes:
        return

    if cube_name in split_cubes:
        year_list = (
            cube_model.objects.all().distinct().values_list("financial_year", flat=True)
        )

        if cube_name in all_years_cubes:
            file_names.update(cube_to_files(cube_model, timestamp, with_xlsx=False))

        file_names.update(split_cube_to_files(cube_model, timestamp, year_list))
    else:
        file_names.update(cube_to_files(cube_model, timestamp))

    save_metadata(file_names, cube_name, timestamp)


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


def xlsx_allowed(cube_name, row_count):
    return cube_name not in disable_xlsx and row_count <= xlsx_max_rows


def cube_to_files(cube_model, timestamp, with_xlsx=True):
    cube_name = cube_model._meta.db_table
    cube = get_cube(cubes_map[cube_name])
    field_refs, rows = stream_cube_facts(cube)
    headers = field_labels(cube, field_refs)
    write_xlsx = with_xlsx and xlsx_allowed(cube_name, cube_model.objects.count())
    file_names = write_facts(
        headers, rows, cube_name, f"{cube_name}_{timestamp}", write_xlsx
    )
    return {all_years: file_names}


def split_cube_to_files(cube_model, timestamp, year_list):
    cube_name = cube_model._meta.db_table
    cube = get_cube(cubes_map[cube_name])
    files = {}

    for year in year_list:
        field_refs, rows = stream_cube_facts(
            cube, cuts=f"financial_year_end.year:{year}"
        )
        headers = field_labels(cube, field_refs)
        write_xlsx = xlsx_allowed(
            cube_name, cube_model.objects.filter(financial_year=year).count()
        )
        files[year] = write_facts(
            headers, rows, cube_name, f"{cube_name}_{year}__{timestamp}", write_xlsx
        )
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


def storage_path(cube_name, file_name):
    return f"{settings.BULK_DOWNLOAD_DIR}/{cube_name}/{file_name}"


def write_facts(headers, rows, cube_name, base_name, write_xlsx):
    """Write the streamed facts to csv, and to xlsx alongside it when write_xlsx
    is set. Both formats are written from a single pass over the rows, because
    rows is a one-shot generator and reading it again means a second scan of the
    fact table. Returns the names of the files written."""
    csv_name = f"{base_name}.csv"
    file_names = [csv_name]

    with default_storage.open(storage_path(cube_name, csv_name), "wb") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

        if not write_xlsx:
            for fact in rows:
                writer.writerow(fact.values())
            return file_names

        xlsx_name = f"{base_name}.xlsx"
        with default_storage.open(
            storage_path(cube_name, xlsx_name), "wb"
        ) as xlsx_file:
            # constant_memory writes each row to disk instead of holding the
            # whole sheet in memory
            workbook = xlsxwriter.Workbook(
                xlsx_file,
                {
                    "constant_memory": True,
                    "strings_to_formulas": False,
                    "strings_to_urls": False,
                },
            )
            worksheet = workbook.add_worksheet()

            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header)

            row_num = 1
            for fact in rows:
                values = list(fact.values())
                writer.writerow(values)
                for col_num, value in enumerate(values):
                    worksheet.write(row_num, col_num, value)
                row_num += 1

            workbook.close()

    file_names.append(xlsx_name)
    return file_names


def save_metadata(file_names, cube_name, timestamp):
    file_metadata = {}
    for file_year in file_names:
        file_metadata[file_year] = []
        for name in file_names[file_year]:
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            size = 0
            with default_storage.open(storage_path(cube_name, name), "rb") as f:
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

    with default_storage.open(storage_path(cube_name, metadata_index), "w") as file:
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
