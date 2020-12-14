
import csv

from collections import namedtuple

from ..models import (
    AgedDebtorItemsV2,
    AgedDebtorFactsV2,
    AmountTypeV2,
)

from .utils import (
    Updater,
    period_code_details,
    build_unique_query_params_with_period,
)


AgedDebtorFactRow = namedtuple(
    "AgedDebtorFactRow",
    (
        "demarcation_code",
        "period_code",
        "customer_group_code",
        "item_code",
        "l30_amount",
        "l60_amount",
        "l90_amount",
        "l120_amount",
        "l150_amount",
        "l180_amount",
        "l1_amount",
        "g1_amount",
        "total_amount",
        "bad_amount",
        "badi_amount",
    ),
)


class AgedDebtorFactsReader(object):

    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(AgedDebtorFactRow._make, self._reader):
            yield row


class AgedDebtorFactsUpdater(Updater):
    facts_cls = AgedDebtorFactsV2
    reader_cls = AgedDebtorFactsReader
    references_cls = {
        "items": AgedDebtorItemsV2,
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
        item = self.references["items"][row.item_code]
        amount_type = self.references["amount_types"][amount_type_code]
        return self.facts_cls(
            demarcation_code=row.demarcation_code,
            period_code=row.period_code,
            financial_year=financial_year,
            financial_period=financial_period,
            period_length=period_length,
            item=item,
            amount_type=amount_type,
            customer_group_code=row.customer_group_code,
            bad_amount=int(float(row.bad_amount)),
            badi_amount=int(float(row.badi_amount)),
            g1_amount=int(float(row.g1_amount)),
            l1_amount=int(float(row.l1_amount)),
            l120_amount=int(float(row.l120_amount)),
            l150_amount=int(float(row.l150_amount)),
            l180_amount=int(float(row.l180_amount)),
            l30_amount=int(float(row.l30_amount)),
            l60_amount=int(float(row.l60_amount)),
            l90_amount=int(float(row.l90_amount)),
            total_amount=int(float(row.total_amount)),
        )


def update_aged_debtor_facts_v2(update_obj, batch_size):
    updater = AgedDebtorFactsUpdater(update_obj, batch_size)
    updater.update()
