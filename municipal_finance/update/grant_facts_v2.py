
import csv

from collections import namedtuple

from ..models import (
    AmountTypeV2,
    GrantTypesV2,
    GrantFactsV2,
)

from .utils import (
    Updater,
    period_code_details,
    build_unique_query_params_with_period,
)


GrantFactRow = namedtuple(
    "GrantFactRow",
    (
        "demarcation_code",
        "period_code",
        "grant_type_code",
        "amount",
    ),
)


class GrantFactsReader(object):

    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(GrantFactRow._make, self._reader):
            yield row


class GrantFactsUpdater(Updater):
    facts_cls = GrantFactsV2
    reader_cls = GrantFactsReader
    references_cls = {
        "amount_types": AmountTypeV2,
        "grant_types": GrantTypesV2,
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
        amount_type = self.references["amount_types"][amount_type_code]
        grant_type = self.references["grant_types"][row.grant_type_code]
        return self.facts_cls(
            demarcation_code=row.demarcation_code,
            period_code=row.period_code,
            financial_year=financial_year,
            financial_period=financial_period,
            period_length=period_length,
            amount=amount,
            amount_type=amount_type,
            grant_type=grant_type,
        )


def update_grant_facts_v2(update_obj, batch_size):
    updater = GrantFactsUpdater(update_obj, batch_size)
    updater.update()
