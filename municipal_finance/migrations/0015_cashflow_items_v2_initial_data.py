# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from . import run_data_import

from ..resources import CashflowItemsV2Resource


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0014_amount_type_v2_initial_data'),
    ]

    operations = [
        run_data_import(CashflowItemsV2Resource, 'cash_flow_items_v2.csv'),
    ]
