# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tablib

from django.db import migrations, models

from ..resources import BsheetItemsV1Resource


def import_initial_data(apps, schema_editor):
    dataset = tablib.Dataset().load(
        open('municipal_finance/fixtures/initial/bsheet_items_v1.csv')
    )
    BsheetItemsV1Resource().import_data(dataset, raise_errors=True)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0018_financial_position_items_v2_initial_data'),
    ]

    operations = [
        migrations.RunPython(import_initial_data)
    ]
