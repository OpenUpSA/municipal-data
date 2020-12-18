# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from . import run_data_import

from ..resources import GovernmentFunctionsV2Resource


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0015_cashflow_items_v2_initial_data'),
    ]

    operations = [
        run_data_import(
            GovernmentFunctionsV2Resource, 'government_functions_v2.csv',
        ),
    ]
