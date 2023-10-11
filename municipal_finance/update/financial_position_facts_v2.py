
import csv

from collections import namedtuple

from ..models import (
    AmountTypeV2,
    FinancialPositionItemsV2,
    FinancialPositionFactsV2,
)

from .utils import (
    Updater,
    period_code_details,
    build_unique_query_params_with_period,
)


FinancialPositionFactRow = namedtuple(
    "FinancialPositionFactRow",
    (
        "demarcation_code",
        "period_code",
        "item_code",
        "amount",
    ),
)


class FinancialPositionFactsReader(object):

    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(FinancialPositionFactRow._make, self._reader):
            yield row


class FinancialPositionFactsUpdater(Updater):
    facts_cls = FinancialPositionFactsV2
    reader_cls = FinancialPositionFactsReader
    references_cls = {
        "items": FinancialPositionItemsV2,
        "amount_types": AmountTypeV2,
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
        return self.facts_cls(
            demarcation_code=row.demarcation_code,
            period_code=row.period_code,
            financial_year=financial_year,
            financial_period=financial_period,
            period_length=period_length,
            amount=amount,
            amount_type=amount_type,
            item=item,
        )


def update_financial_position_facts_v2(update_obj, batch_size, **kwargs):
    updater = FinancialPositionFactsUpdater(update_obj, batch_size)
    updater.update()
