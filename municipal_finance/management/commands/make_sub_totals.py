from django.core.management.base import BaseCommand, CommandError

from municipal_finance.models import (
    FinancialPositionFactsV2,
    FinancialPositionItemsV2,
    AmountTypeV2,
)
from scorecard.models import MunicipalityProfile


# This is supposed to be a temporary fix to add sub-totals to the cubes


class Command(BaseCommand):
    help = "Make sub totals"

    def handle(self, *args, **options):
        total_items = {
            "0190": [
                "0120",
                "0130",
                "0140",
                "0150",
                "0160",
                "0170",
                "0180",
            ],
            "0310": [
                "0210",
                "0220",
                "0230",
                "0240",
                "0250",
                "0260",
                "0270",
                "0280",
                "0290",
                "0300",
            ],
            "0320": ["0190", "0310"],
            "0430": ["0350", "0360", "0370", "0380", "0390", "0400", "0410", "0420"],
            "0490": ["0450", "0460", "0470", "0480"],
            "0500": ["0430", "0490"],
            "0510": ["0320", "0500"],
            "0560": ["0530", "0540", "0550"],
        }

        year_list = ["2018", "2019", "2020", "2021", "2022"]

        demarcation_codes = MunicipalityProfile.objects.values_list(
            "demarcation_code", flat=True
        )
        demarcation_codes_list = list(demarcation_codes)
        # demarcation_codes_list = ["BUF", "TSH"]

        amount_types = AmountTypeV2.objects.values_list("id", flat=True)
        amount_types_list = list(amount_types)
        # amount_types_list = ['1','2',]

        for fin_year in year_list:
            for item_key in total_items:
                for muni_code in demarcation_codes_list:
                    for amount_type in amount_types_list:
                        sub_total = 0
                        for item in total_items[item_key]:
                            finpos = FinancialPositionFactsV2.objects.filter(
                                financial_year=fin_year,
                                item_id__code=item,
                                demarcation_code=muni_code,
                                amount_type=amount_type,
                            )
                            if finpos:
                                if finpos[0].amount:
                                    sub_total += finpos[0].amount

                        amount_type_model = AmountTypeV2.objects.get(id=amount_type)
                        item_code = FinancialPositionItemsV2.objects.get(code=item_key)

                        if sub_total != 0:
                            FinancialPositionFactsV2.objects.update_or_create(
                                financial_year=fin_year,
                                financial_period=fin_year,
                                period_code=f"{fin_year}{amount_type_model.code}",
                                item_id=item_code.id,
                                demarcation_code=muni_code,
                                amount_type=amount_type_model,
                                period_length="year",
                                defaults={
                                    'amount': sub_total,
                                }
                            )
