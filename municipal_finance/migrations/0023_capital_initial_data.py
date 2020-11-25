# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from . import run_data_import

from ..resources import (
    CapitalTypeV2Resource,
    CapitalItemsV1Resource,
    CapitalItemsV2Resource,
)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0022_auto_20201125_0906'),
    ]

    operations = [
        run_data_import(CapitalTypeV2Resource, 'capital_type_v2.csv'),
        run_data_import(CapitalItemsV1Resource, 'capital_items_v1.csv'),
        run_data_import(CapitalItemsV2Resource, 'capital_items_v2.csv'),
    ]
