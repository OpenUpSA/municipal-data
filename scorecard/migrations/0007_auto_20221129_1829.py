# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-11-29 16:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0006_geographyupdate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='geography',
            options={'verbose_name': 'Municipality', 'verbose_name_plural': 'Municipalities'},
        ),
    ]
