# Generated by Django 2.2.28 on 2023-06-14 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import municipal_finance.models.updates


def add_new_schema(apps, schema_editor):
    schema = apps.get_model('municipal_finance', 'ItemCodeSchema')
    version = schema(version=0)
    version.save()


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0044_portal_data_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='agedcreditorfactsv2update',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='agedcreditorfactsv2update',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='ageddebtorfactsv2update',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='ageddebtorfactsv2update',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='auditopinionfactsupdate',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='auditopinionfactsupdate',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='capitalfactsv2update',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='capitalfactsv2update',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='cashflowv2update',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cashflowv2update',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='financialpositionfactsv2update',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='financialpositionfactsv2update',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='grantfactsv2update',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='grantfactsv2update',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='incomeexpenditurev2update',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='incomeexpenditurev2update',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='municipalstaffcontactsupdate',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='municipalstaffcontactsupdate',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='repairsmaintenancev2update',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='repairsmaintenancev2update',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='uifwexpensefactsupdate',
            name='import_report',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='uifwexpensefactsupdate',
            name='task_id',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.CreateModel(
            name='ItemCodeSchema',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('task_id', models.TextField(editable=False, null=True)),
                ('version', models.CharField(max_length=10, unique=True)),
                ('file', models.FileField(max_length=255, upload_to=municipal_finance.models.updates.UpdateFilePath())),
            ],
            options={
                'verbose_name': 'Item Code Schema',
                'db_table': 'item_code_schema',
            },
        ),
        migrations.RunPython(add_new_schema),
    ]
