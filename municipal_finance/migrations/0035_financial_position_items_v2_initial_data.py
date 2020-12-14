# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from . import run_data_import

from ..resources import FinancialPositionItemsV2Resource


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0034_auto_20201214_1607'),
    ]

    operations = [
        run_data_import(
            FinancialPositionItemsV2Resource,
            'financial_position_items_v2.csv',
        ),
    ]
