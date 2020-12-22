# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from . import run_data_import

from ..resources import AmountTypeV2Resource


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0013_auto_20201113_0957'),
    ]

    operations = [
        run_data_import(AmountTypeV2Resource, 'amount_type_v2.csv'),
    ]
