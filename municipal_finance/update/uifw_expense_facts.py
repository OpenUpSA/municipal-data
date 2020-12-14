
import csv

from collections import namedtuple

from ..models import (
    AmountTypeV2,
    UIFWExpenseFacts,
)

from .utils import (
    Updater,
    period_code_details,
    build_unique_query_params_with_year,
)


UIFWExpensesFactRow = namedtuple(
    "UIFWExpensesFactRow",
    (
        "demarcation_code",
        "financial_year",
        "item_code",
        "item_label",
        "amount",
    ),
)


class UIFWExpensesFactsReader(object):

    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(UIFWExpensesFactRow._make, self._reader):
            yield row


class FinancialPositionFactsUpdater(Updater):
    facts_cls = UIFWExpenseFacts
    reader_cls = UIFWExpensesFactsReader
    references_cls = {}

    def build_unique_query(self, rows):
        return build_unique_query_params_with_year(rows)

    def row_to_obj(self, row):
        amount = int(row.amount) if row.amount else None
        return self.facts_cls(
            demarcation_code=row.demarcation_code,
            financial_year=row.financial_year,
            item_code=row.item_code,
            item_label=row.item_label,
            amount=amount,
        )


def update_uifw_expense_facts(update_obj, batch_size):
    updater = FinancialPositionFactsUpdater(update_obj, batch_size)
    updater.update()
