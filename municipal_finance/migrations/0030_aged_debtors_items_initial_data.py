# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from . import run_data_import

from ..resources import (
    AgedDebtorItemsV1Resource,
    AgedDebtorItemsV2Resource,
)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0029_auto_20201206_1342'),
    ]

    operations = [
        run_data_import(
            AgedDebtorItemsV1Resource,
            'aged_debtor_items_v1.csv',
        ),
        run_data_import(
            AgedDebtorItemsV2Resource,
            'aged_debtor_items_v2.csv',
        ),
    ]
