# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from . import run_data_import

from ..resources import IncexpItemsV2Resource


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0016_government_functions_v2_initial_data'),
    ]

    operations = [
        run_data_import(
            IncexpItemsV2Resource, 'income_expenditure_items_v2.csv',
        ),
    ]
