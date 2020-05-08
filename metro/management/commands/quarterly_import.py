from django.core.management.base import BaseCommand, CommandError
import csv

from scorecard.models import Geography
from metro import models


class Command(BaseCommand):
    help = "Import quarterly results"

    def add_arguments(self, parser):
        parser.add_argument("file_path")
        parser.add_argument("--geo_code")
        parser.add_argument("--budget_year")
        parser.add_argument("--quarter")

    def handle(self, *args, **options):
        try:
            quarter_dict = {}
            geography = Geography.objects.get(geo_code=options["geo_code"])
            financial_year = models.FinancialYear.objects.get(
                budget_year=options["budget_year"]
            )
        except (Geography.DoesNotExist, models.FinancialYear.DoesNotExist):
            raise CommandError("Geography or Financial Year does not exist")
        with open(options["file_path"], "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row["Performance indicator"]:
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Working on  "%s"' % row["Performance indicator"]
                        )
                    )
                    try:
                        indicator = models.Indicator.objects.get(
                            code=row["Performance indicator"]
                        )
                    except models.Indicator.DoesNotExist:
                        raise CommandError(
                            "Indicator code does not exists, perhaps add it first"
                        )
                    else:
                        indicator.target = row["Annual target"]
                        indicator.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                'Success on  "%s"' % row["Performance indicator"]
                            )
                        )
                        if options["quarter"] == "1":
                            models.IndicatorQuarterResult.objects.create(
                                indicator=indicator,
                                geography=geography,
                                financial_year=financial_year,
                                quarter_one=row["Output"],
                            )

                        elif options["quarter"] == "2":
                            models.IndicatorQuarterResult.objects.create(
                                indicator=indicator,
                                geography=geography,
                                financial_year=financial_year,
                                quarter_two=row["Output"],
                            )

                        elif options["quarter"] == "3":
                            models.IndicatorQuarterResult.objects.create(
                                indicator=indicator,
                                geography=geography,
                                financial_year=financial_year,
                                quarter_three=row["Output"],
                            )

                        elif options["quarter"] == "4":
                            models.IndicatorQuarterResult.objects.create(
                                indicator=indicator,
                                geography=geography,
                                financial_year=financial_year,
                                quarter_four=row["Output"],
                            )
