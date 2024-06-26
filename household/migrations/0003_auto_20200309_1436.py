# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-03-09 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSetFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to='datasets/')),
            ],
        ),
        migrations.CreateModel(
            name='DataSetVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(default=1, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='datasetfile',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.DataSetVersion'),
        ),
        migrations.AddField(
            model_name='householdbill',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='household.DataSetVersion'),
        ),
        migrations.AddField(
            model_name='householdincrease',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='household.DataSetVersion'),
        ),
    ]
