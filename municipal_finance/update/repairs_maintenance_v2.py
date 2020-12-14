
import csv
import requests

from functools import reduce
from collections import namedtuple
from contextlib import closing

from django.db import transaction

from ..models import (
    RepairsMaintenanceItemsV2,
    RepairsMaintenanceFactsV2,
    AmountTypeV2,
)

from .utils import (
    all_to_code_dict,
    period_code_details,
    group_rows,
    delete_existing,
)


RepairsMaintenanceRow = namedtuple(
    "RepairsMaintenanceRow",
    (
        "demarcation_code",
        "period_code",
        "item_code",
        "amount",
    ),
)


class RepairsMaintenanceReader(object):

    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(RepairsMaintenanceRow._make, self._reader):
            yield row


def row_to_obj(amount_types, items, row: RepairsMaintenanceRow):
    (
        financial_year,
        amount_type_code,
        period_length,
        financial_period
    ) = period_code_details(row.period_code)
    amount = int(row.amount) if row.amount else None
    item = items[row.item_code]
    amount_type = amount_types[amount_type_code]
    return RepairsMaintenanceFactsV2(
        demarcation_code=row.demarcation_code,
        period_code=row.period_code,
        financial_year=financial_year,
        financial_period=financial_period,
        period_length=period_length,
        amount=amount,
        amount_type=amount_type,
        item=item,
    )


def update_repairs_maintenance_v2(update_obj, batch_size):
    with transaction.atomic():
        # Collect the required references
        amount_types = all_to_code_dict(AmountTypeV2)
        items = all_to_code_dict(RepairsMaintenanceItemsV2)
        # Delete the existing matching records
        deleted = delete_existing(
            update_obj,
            RepairsMaintenanceFactsV2,
            RepairsMaintenanceReader,
            batch_size,
        )
        # Add the records from the dataset
        inserted = 0
        update_obj.file.open('r')
        with closing(update_obj.file) as file:
            lines = iter(file)
            next(lines)  # Skip header
            reader = RepairsMaintenanceReader(lines)
            for rows in group_rows(reader, batch_size):
                objects = map(
                    lambda row: row_to_obj(
                        amount_types, items, row
                    ),
                    filter(None, rows),
                )
                objects = RepairsMaintenanceFactsV2.objects.bulk_create(
                    objects
                )
                inserted += len(objects)
        update_obj.deleted = deleted
        update_obj.inserted = inserted
        update_obj.save()
