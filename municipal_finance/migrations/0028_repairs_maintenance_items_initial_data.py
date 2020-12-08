# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from . import run_data_import

from ..resources import (
    RepairsMaintenanceItemsV1Resource,
    RepairsMaintenanceItemsV2Resource,
)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0027_auto_20201206_1123'),
    ]

    operations = [
        run_data_import(
            RepairsMaintenanceItemsV1Resource,
            'repairs_maintenance_items_v1.csv',
        ),
        run_data_import(
            RepairsMaintenanceItemsV2Resource,
            'repairs_maintenance_items_v2.csv',
        ),
    ]
