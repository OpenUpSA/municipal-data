# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-06 12:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0018_auto_20210928_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='latest_implementation_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infrastructure.FinancialYear'),
        ),
    ]
