import csv
import unittest
from infrastructure import models
from scorecard.models import Geography
from django.db import transaction

headers = [
    x.strip()
    for x in """
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
""".split(
        ","
    )
]


def float_or_none(val):
    try:
        return float(val)
    except ValueError:
        return None


def check_file(fp):
    reader = csv.DictReader(fp)
    fields = reader.fieldnames[0:12]

    if fields != headers:
        raise ValueError(
            "Expected these fields as input: \n%s. Received: \n%s" % (headers, fields)
        )


@transaction.atomic
def load_file(geography, fp):
    check_file(fp)
    fp.seek(0)
    reader = csv.DictReader(fp)

    additional_fields = list(reader.fieldnames[12:])
    for field in additional_fields:
        create_finance_phase(field)

    for idx, row in enumerate(reader):
        try:
            p = models.Project.objects.create(
                geography=geography,
                function=row["Function"],
                project_description=row["Project Description"],
                project_number=row["Project Number"],
                project_type=row["Type"],
                mtsf_service_outcome=row["MTSF Service Outcome"],
                iudf=row["IUDF"],
                own_strategic_objectives=row["Own Strategic Objectives"],
                asset_class=row["Asset Class"],
                asset_subclass=row["Asset Sub-Class"],
                ward_location=row["Ward Location"],
                longitude=float_or_none(row["GPS Longitude"]),
                latitude=float_or_none(row["GPS Latitude"]),
            )

            for field in additional_fields:
                amount = row[field]
                create_expenditure(p, field, amount)
        except Exception as e:
            raise ValueError("Error loading data in row: %d - %s" % (idx + 2, row))
    return idx + 1


def create_expenditure(project, finance_phase, amount):
    phase, year = create_finance_phase(finance_phase)
    try:
        expenditure = models.Expenditure.objects.create(
            project=project,
            budget_phase=phase,
            financial_year=year,
            amount=float(amount),
        )
        return True
    except ValueError:
        return False


def create_finance_phase(s):
    phase, year = parse_finance_phase(s)
    fy, _ = models.FinancialYear.objects.get_or_create(budget_year=year)
    phase, _ = models.BudgetPhase.objects.get_or_create(name=phase)

    return phase, fy


def parse_finance_phase(s):
    parts = s.split()
    year = parts[-1]

    y1, y2 = year.split("/")
    if len(y2) == 2:
        y2 = str(int(y1) + 1)

    year = "%s/%s" % (y1, y2)

    return " ".join(parts[0:-1]), year
