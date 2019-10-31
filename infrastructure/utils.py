import csv
import unittest
from infrastructure import models
from scorecard.models import Geography
from django.db import transaction

headers = [x.strip() for x in """
    Function,
    Project Description,
    Project Number,
    Type,
    MTSF Service Outcome,
    IUDF,
    Own Strategic Objectives,
    Asset Class,
    Asset Sub-Class,
    Ward Location,
    GPS Longitude,
    GPS Latitude
""".split(",")]

def float_or_none(val):
    try:
        return float(val)
    except ValueError:
        return Nonej

def check_file(fp):
    reader = csv.DictReader(fp)

    if reader.fieldnames != headers:
        raise ValueError("Expected these fields as input: %s. Received: %s" % (headers, reader.fieldnames))

@transaction.atomic
def load_file(geography, fp):
    check_file(fp)
    fp.seek(0)
    reader = csv.DictReader(fp)
    for idx, row in enumerate(reader):
        try:
            p = models.Project.objects.create(
                geography=geography,
                function=row["Function"], project_description=row["Project Description"], project_number=row["Project Number"],
                project_type=row["Type"], mtsf_service_outcome=row["MTSF Service Outcome"], iudf=row["IUDF"],
                own_strategic_objectives=row["Own Strategic Objectives"], asset_class=row["Asset Class"], asset_subclass=row["Asset Sub-Class"],
                ward_location=row["Ward Location"], longitude=float(row["GPS Longitude"]), latitude=float(row["GPS Latitude"])
            )
        except ValueError as e:
            raise ValueError("Error loading data in row: %d - %s" % (idx + 2, row))

