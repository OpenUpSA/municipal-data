import csv
import boto3
from io import StringIO
import tempfile
import logging

from django.conf import settings
from .models import (
    HouseholdServiceTotal,
    HouseholdBillTotal,
    DataSetFile,
    BudgetPhase,
    HouseholdService,
    FinancialYear,
    HouseholdClass,
)
from scorecard.models import Geography
from django.db import transaction
from django.db import IntegrityError


log = logging.getLogger("household.upload")


def amazon_s3(file_name):
    """
    Get file from amazon and process
    """
    temp_file = tempfile.NamedTemporaryFile()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3.download_fileobj(
        settings.AWS_STORAGE_BUCKET_NAME, "media/" + file_name, temp_file
    )

    return temp_file


def import_bill_data(id):
    """
    get file and pass to apporiate model
    """
    csv_obj = DataSetFile.objects.get(id=id)
    if csv_obj.file_type == "Service":
        household_service_total(csv_obj)
        log.info("Found correct csv Service bill, moving to Service Total")
    elif csv_obj.file_type == "Bill":
        print("Found correct bill, moving to Bill Totals")
        log.info("Found correct bill, moving to Bill Totals")
        household_bill_total(csv_obj)
    else:
        log.error("Unknown household csv type")
        raise Exception("csv type unknown")


@transaction.atomic
def household_service_total(csv_obj):
    log.info("Working on service totals")
    csv_file = csv_obj.csv_file.read().decode("utf-8")
    csv_data = csv.DictReader(StringIO(csv_file))

    HouseholdServiceTotal.objects.all().delete()

    for row in csv_data:
        geography = Geography.objects.get(geo_code=row["Geography"])
        financial_year = FinancialYear.objects.get(
            budget_year=row["Financial Year"]
        )
        budget_phase = BudgetPhase.objects.get(name=row["Budget Phase"])
        household_class = HouseholdClass.objects.get(name=row["Class"])
        service = HouseholdService.objects.get(name=row["Service Name"])
        total = row["Total"] if row["Total"] else None
        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=financial_year,
            budget_phase=budget_phase,
            household_class=household_class,
            service=service,
            total=total,
        )
    log.info("Completed working on service totals")


@transaction.atomic
def household_bill_total(csv_obj):
    log.info("Working on total bill totals")
    csv_file = csv_obj.csv_file.read().decode("utf-8")
    csv_data = csv.DictReader(StringIO(csv_file))

    HouseholdBillTotal.objects.all().delete()

    for row in csv_data:
        geography = Geography.objects.get(geo_code=row["Geography"])
        financial_year = FinancialYear.objects.get(
            budget_year=row["Financial Year"]
        )
        budget_phase = BudgetPhase.objects.get(name=row["Budget Phase"])
        household_class = HouseholdClass.objects.get(name=row["Class"])
        percent = row["Percent Increase"] if row["Percent Increase"] else None
        total = row["Total"] if row["Total"] else None
        HouseholdBillTotal.objects.create(
            geography=geography,
            financial_year=financial_year,
            budget_phase=budget_phase,
            household_class=household_class,
            percent=percent,
            total=total,
        )
    log.info("Completed working on bill totals")
