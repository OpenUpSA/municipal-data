# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tablib

from django.db import migrations, models

from ..resources import (
    CashflowItemsV1Resource,
    AmountTypeV1Resource,
    IncexpItemsV1Resource,
    GovernmentFunctionsV1Resource,
)


def run_data_import(resource, filename):

    def import_initial_data(apps, schema_editor):
        dataset = tablib.Dataset().load(
            open(f'municipal_finance/fixtures/initial/{filename}'),
            format='csv',
            headers=True,
        )
        resource().import_data(dataset, raise_errors=True)

    return migrations.RunPython(import_initial_data)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0019_bsheet_items_v1_initial_data'),
    ]

    operations = [
        run_data_import(CashflowItemsV1Resource, 'cflow_items_v1.csv'),
        run_data_import(AmountTypeV1Resource, 'amount_type_v1.csv'),
        run_data_import(IncexpItemsV1Resource, 'incexp_items_v1.csv'),
        run_data_import(GovernmentFunctionsV1Resource,
                        'government_functions_v1.csv'),
    ]
