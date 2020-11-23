# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tablib

from django.db import migrations, models

from ..resources import AmountTypeV2Resource


def import_initial_data(apps, schema_editor):
    dataset = tablib.Dataset().load(
        open('municipal_finance/fixtures/initial/amount_type_v2.csv'),
        format='csv',
        headers=True,
    )
    AmountTypeV2Resource().import_data(dataset, raise_errors=True)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0013_auto_20201113_0957'),
    ]

    operations = [
        migrations.RunPython(import_initial_data)
    ]
