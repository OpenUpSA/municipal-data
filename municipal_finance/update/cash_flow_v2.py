from django.db.models import Max
import csv
import requests

from functools import reduce
from collections import namedtuple
from contextlib import closing

from django.db import transaction

from ..models import (
    CflowItemsV2,
    CflowFactsV2,
    AmountTypeV2,
)

from .utils import (
    Updater,
    build_unique_query_params_with_period,
    period_code_details,
)


CashFlowFactRow = namedtuple(
    "CashFlowFactRow",
    (
        "demarcation_code",
        "period_code",
        "item_code",
        "amount",
    ),
)


class CashFlowFactsReader(object):
    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(CashFlowFactRow._make, self._reader):
            yield row


class CashFlowFactsV2Updater(Updater):
    facts_cls = CflowFactsV2
    reader_cls = CashFlowFactsReader
    references_cls = {
        "amount_types": AmountTypeV2,
        "items": CflowItemsV2,
    }
    schema_version = references_cls["items"].objects.aggregate(version=Max("version"))[
        "version"
    ]
    ref_items = references_cls["items"].objects.filter(version=schema_version)
    item_map = {}
    for item in ref_items:
        item_map[str(item)] = item

    def build_unique_query(self, rows):
        return build_unique_query_params_with_period(rows)

    def row_to_obj(self, row: CashFlowFactRow):
        (
            financial_year,
            amount_type_code,
            period_length,
            financial_period,
        ) = period_code_details(row.period_code)
        amount = int(row.amount) if row.amount else None
        item = self.item_map["items"][row.item_code]
        amount_type = self.references["amount_types"][amount_type_code]
        return CflowFactsV2(
            demarcation_code=row.demarcation_code,
            period_code=row.period_code,
            financial_year=financial_year,
            financial_period=financial_period,
            period_length=period_length,
            amount=amount,
            amount_type=amount_type,
            item=item,
        )


def update_cash_flow_v2(update_obj, batch_size, **kwargs):
    updater = CashFlowFactsV2Updater(update_obj, batch_size)
    updater.update()
