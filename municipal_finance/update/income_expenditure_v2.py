
import csv
import requests

from collections import namedtuple
from contextlib import closing

from django.db import transaction

from ..models import (
    IncexpItemsV2,
    IncexpFactsV2,
    AmountTypeV2,
    GovernmentFunctionsV2,
)

from .utils import (
    Updater,
    build_unique_query_params_with_period,
    period_code_details,
)


IncomeExpenditureFactRow = namedtuple(
    "IncomeExpenditureFactRow",
    (
        "demarcation_code",
        "period_code",
        "function_code",
        "item_code",
        "amount",
    ),
)


class IncomeExpenditureFactsReader(object):

    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(IncomeExpenditureFactRow._make, self._reader):
            yield row


class IncomeExpenditureFactsV2Updater(Updater):
    facts_cls = IncexpFactsV2
    reader_cls = IncomeExpenditureFactsReader
    references_cls = {
        "amount_types": AmountTypeV2,
        "items": IncexpItemsV2,
        "functions": GovernmentFunctionsV2,
    }

    def build_unique_query(self, rows):
        return build_unique_query_params_with_period(rows)

    def row_to_obj(self, row: IncomeExpenditureFactRow):
        (
            financial_year,
            amount_type_code,
            period_length,
            financial_period
        ) = period_code_details(row.period_code)
        amount = int(row.amount) if row.amount else None
        item = self.references["items"][row.item_code]
        function = self.references["functions"][row.function_code]
        amount_type = self.references["amount_types"][amount_type_code]
        return IncexpFactsV2(
            demarcation_code=row.demarcation_code,
            period_code=row.period_code,
            financial_year=financial_year,
            financial_period=financial_period,
            period_length=period_length,
            amount=amount,
            amount_type=amount_type,
            item=item,
            function=function,
        )


def update_income_expenditure_v2(update_obj, batch_size):
    updater = IncomeExpenditureFactsV2Updater(
        update_obj, batch_size,
    )
    updater.update()
