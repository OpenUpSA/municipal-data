# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from . import run_data_import

from ..resources import (
    AgedCreditorItemsV1Resource,
    AgedCreditorItemsV2Resource,
)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0042_set_indexes'),
    ]

    operations = [
        run_data_import(
            AgedCreditorItemsV1Resource,
            'aged_creditor_items_v1.csv',
        ),
        run_data_import(
            AgedCreditorItemsV2Resource,
            'aged_creditor_items_v2.csv',
        ),
    ]
