# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import municipal_finance.models.updates

from . import run_data_import

from ..resources import CashflowItemsV2Resource

def add_new_schema(apps, schema_editor):
    schema = apps.get_model('municipal_finance', 'ItemCodeSchema')
    version = schema(id=1, version=1)
    version.save()
    version = schema.objects.get(version=0)
    print("______a______")
    print(version.id)
    print(version.version)
    print("______a______")


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0014_amount_type_v2_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCodeSchema',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('task_id', models.TextField(editable=False, null=True)),
                ('version', models.CharField(max_length=10, unique=True)),
                ('file', models.FileField(max_length=255, upload_to=municipal_finance.models.updates.UpdateFilePath())),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Item Code Schema',
                'db_table': 'item_code_schema',
            },
        ),
        migrations.RunPython(add_new_schema),
        run_data_import(CashflowItemsV2Resource, 'cash_flow_items_v2.csv'),
    ]
