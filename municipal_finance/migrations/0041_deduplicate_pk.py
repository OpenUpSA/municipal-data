# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0023_capital_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ConditionalGrants',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=False, serialize=False),
        ),
    ]
