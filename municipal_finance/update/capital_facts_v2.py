
import csv

from collections import namedtuple

from ..models import (
    AmountTypeV2,
    GovernmentFunctionsV2,
    CapitalTypeV2,
    CapitalItemsV2,
    CapitalFactsV2,
)

from .utils import (
    Updater,
    period_code_details,
    build_unique_query_params_with_period,
)


CapitalFactRow = namedtuple(
    "CapitalFactRow",
    (
        "demarcation_code",
        "period_code",
        "function_code",
        "item_code",
        "capital_type_code",
        "amount",
    ),
)


class CapitalFactsReader(object):

    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(CapitalFactRow._make, self._reader):
            yield row


class CapitalFactsV2Updater(Updater):
    facts_cls = CapitalFactsV2
    reader_cls = CapitalFactsReader
    references_cls = {
        "items": CapitalItemsV2,
        "amount_types": AmountTypeV2,
        "functions": GovernmentFunctionsV2,
        "capital_types": CapitalTypeV2,
    }

    def build_unique_query(self, rows):
        return build_unique_query_params_with_period(rows)

    def row_to_obj(self, row):
        (
            financial_year,
            amount_type_code,
            period_length,
            financial_period
        ) = period_code_details(row.period_code)
        amount = int(row.amount) if row.amount else None
        item = self.references["items"][row.item_code]
        amount_type = self.references["amount_types"][amount_type_code]
        function = self.references["functions"][row.function_code]
        capital_type = self.references["capital_types"][row.capital_type_code]
        return self.facts_cls(
            demarcation_code=row.demarcation_code,
            period_code=row.period_code,
            financial_year=financial_year,
            financial_period=financial_period,
            period_length=period_length,
            amount=amount,
            amount_type=amount_type,
            item=item,
            function=function,
            capital_type=capital_type,
        )


def update_capital_facts_v2(update_obj, batch_size, **kwargs):
    updater = CapitalFactsV2Updater(update_obj, batch_size)
    updater.update()
