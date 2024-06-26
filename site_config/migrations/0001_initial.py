# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-01-10 14:03
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('content', ckeditor.fields.RichTextField()),
                ('notice_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'ordering': ['notice_order'],
            },
        ),
    ]
