# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tablib

from django.db import migrations, models

from ..resources import CashflowItemsMSCOAResource


def import_cashflow_items_mscoa(apps, schema_editor):
    dataset = tablib.Dataset().load(
        open('municipal_finance/fixtures/initial/cashflow_items_mscoa.csv')
    )
    CashflowItemsMSCOAResource().import_data(dataset, raise_errors=True)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0013_auto_20201027_0925'),
    ]

    operations = [
        migrations.RunPython(import_cashflow_items_mscoa)
    ]
