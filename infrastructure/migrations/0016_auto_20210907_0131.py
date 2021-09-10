# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-09-06 23:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0015_financialyear_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnualSpendFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='annual/')),
                ('status', models.IntegerField(default=3)),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infrastructure.FinancialYear')),
            ],
        ),
    ]
