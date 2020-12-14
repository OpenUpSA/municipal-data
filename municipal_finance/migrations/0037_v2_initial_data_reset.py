# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from . import run_data_import

from ..resources import (
    CashflowItemsV2Resource,
    CapitalItemsV2Resource,
    FinancialPositionItemsV2Resource,
    IncexpItemsV2Resource,
    CapitalTypeV2Resource,
    CapitalItemsV1Resource,
)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0036_auto_20201216_1835'),
    ]

    operations = [
        run_data_import(CapitalItemsV1Resource, 'capital_items_v1.csv'),
        run_data_import(CapitalTypeV2Resource, 'capital_type_v2.csv'),
        run_data_import(CashflowItemsV2Resource, 'cash_flow_items_v2.csv'),
        run_data_import(CapitalItemsV2Resource, 'capital_items_v2.csv'),
        run_data_import(FinancialPositionItemsV2Resource,
                        'financial_position_items_v2.csv'),
        run_data_import(IncexpItemsV2Resource,
                        'income_expenditure_items_v2.csv'),
    ]
