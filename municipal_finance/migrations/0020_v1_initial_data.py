# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from . import run_data_import

from ..resources import (
    CashflowItemsV1Resource,
    AmountTypeV1Resource,
    IncexpItemsV1Resource,
    GovernmentFunctionsV1Resource,
)


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
