# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-09-28 11:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.core.exceptions import ObjectDoesNotExist


def populate_implementation_year(apps, schema_editor):
    project = apps.get_model("infrastructure", "Project")
    year = apps.get_model("infrastructure", "FinancialYear")

    db_alias = schema_editor.connection.alias

    try:
        implementation_year_id = year.objects.using(db_alias).get(budget_year="2019/2020").id
    except ObjectDoesNotExist:
        implementation_year_id = 1

    for proj in project.objects.using(db_alias).all():
        proj.latest_implementation_year = implementation_year_id
        proj.save()


def reverse_implementation_year(apps, schema_editor):
    migrations.RemoveField(
        model_name='project',
        name='latest_implementation_year',
    ),


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0016_auto_20210907_0131'),
    ]

    operations = [
        migrations.RunPython(populate_implementation_year, reverse_implementation_year),
        migrations.AddField(
            model_name='project',
            name='latest_implementation_year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='infrastructure.FinancialYear'),
        ),
        migrations.AlterField(
            model_name='annualspendfile',
            name='financial_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infrastructure.FinancialYear', verbose_name='Implementation financial year'),
        ),
    ]
