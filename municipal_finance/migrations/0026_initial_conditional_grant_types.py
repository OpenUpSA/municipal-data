# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from . import run_data_import

from ..resources import (
    ConditionalGrantTypesV1Resource,
    GrantTypesV2Resource,
)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0025_auto_20201207_1032'),
    ]

    operations = [
        run_data_import(
            ConditionalGrantTypesV1Resource,
            'conditional_grant_types_v1.csv',
        ),
        run_data_import(
            GrantTypesV2Resource,
            'grant_types_v2.csv',
        ),
    ]
