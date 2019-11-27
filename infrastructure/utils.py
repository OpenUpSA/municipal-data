import csv
import unittest
from infrastructure import models
from scorecard.models import Geography
from django.db import transaction
import xlrd
import logging

logger = logging.Logger(__name__)

headers = [
    x.strip()
    for x in """
    Function, Project Description, Project Number,
    Type, MTSF Service Outcome, IUDF,
    Own Strategic Objectives, Asset Class, Asset Sub-Class,
    Ward Location, GPS Longitude, GPS Latitude""".strip().split(",")
]
#Audited Outcome 2017/18,
#Full Year Forecast 2018/19,
#Budget year 2019/20,
#Budget year 2020/21,
#Budget year 2021/22


def float_or_none(val):
    try:
        return float(val)
    except ValueError:
        return None


def check_file(fp):
    reader = csv.DictReader(fp)
    return check_headers(reader.fieldnames)

def check_headers(fields):
    missing_headers = [h for h in headers if h not in fields]
    if len(missing_headers) > 0:
        raise ValueError(
            "The following fields are missing from the data source: %s" % missing_headers
        )

@transaction.atomic
def load_excel(filename):
    def clean(s):
        if type(s) == str:
            return s.strip()
        else:
            return s

    def fix_broken_headers(header_row):
        header_row = [r.replace("\n", " ") for r in header_row]
        header_row = [r.replace("Project Decription", "Project Description") for r in header_row]
        return header_row

    def sheet_parser(sheet):
        skip = True
        header_row = []
        for idx in range(0, sheet.nrows):
            row = [clean(sheet.cell(idx, col).value) for col in range(0, sheet.ncols)]

            val = sheet.cell(idx, 0).value.strip()
            if val != "Function" and skip:
                continue 
            elif val == "Function":
                header_row = fix_broken_headers(row)
                check_headers(header_row)
                skip = False
                continue
            elif val == "":
                return

            yield dict(zip(header_row, row))

    workbook = xlrd.open_workbook(filename)
    print(workbook.sheets)
    for sheet in workbook.sheets():
        geo_code = sheet.name
        logger.info("Processing sheet: %s" % sheet.name)
        if Geography.objects.filter(geo_code=geo_code).count() == 0:
            raise CommandError("%s is an unknown Geography. Please ensure that this Geography exists in the database" % geo_code)
        geography = Geography.objects.get(geo_code=geo_code)
        load_file(geography, sheet_parser(sheet))

def load_csv(geography, fp):
    check_file(fp)
    fp.seek(0)
    reader = csv.DictReader(fp)
    return load_file(geography, reader)

@transaction.atomic
def load_file(geography, reader):
    print(geography.geo_code)
    created_phases = False


    for idx, row in enumerate(reader):
        if not created_phases:
            additional_fields = [k for k in row.keys() if k not in headers]
            for field in additional_fields:
                create_finance_phase(field)
            created_phases = True
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
