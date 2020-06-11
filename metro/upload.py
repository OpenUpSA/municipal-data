import csv
from . import models
import io
import logging

log = logging.getLogger(__name__)


def process_file(obj_id):
    """Extract Quarterly data"""
    update = models.UpdateFile.objects.get(id=obj_id)
    csv_file = io.TextIOWrapper(update.document.file)
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row["Performance indicator"]:
            try:
                indicator = models.Indicator.objects.get(
                    code=row["Performance indicator"]
                )
            except models.Indicator.DoesNotExist:
                print(f"Indicator {row['Performance indicator']} does not exist")
                continue
            else:
                if update.quarter == "Q1":
                    models.IndicatorQuarterResult.objects.update_or_create(
                        indicator=indicator,
                        geography=update.geography,
                        financial_year=update.financial_year,
                        defaults={
                            "quarter_one": row["Output"],
                            "target": row["Annual target"],
                        },
                    )

                elif update.quarter == "Q2":
                    models.IndicatorQuarterResult.objects.update_or_create(
                        indicator=indicator,
                        geography=update.geography,
                        financial_year=update.financial_year,
                        defaults={
                            "quarter_two": row["Output"],
                            "target": row["Annual target"],
                        },
                    )

                elif update.quarter == "Q3":
                    models.IndicatorQuarterResult.objects.update_or_create(
                        indicator=indicator,
                        geography=update.geography,
                        financial_year=update.financial_year,
                        defaults={
                            "quarter_three": row["Output"],
                            "target": row["Annual target"],
                        },
                    )

                elif update.quarter == "Q4":
                    models.IndicatorQuarterResult.objects.update_or_create(
                        indicator=indicator,
                        geography=update.geography,
                        financial_year=update.financial_year,
                        defaults={
                            "quarter_four": row["Output"],
                            "target": row["Annual target"],
                        },
                    )
                else:
                    raise ValueError("Financial Quarter does not exist")
    update.status = models.UpdateFile.SUCCESS
    update.save()
