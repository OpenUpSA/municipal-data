# Generated by Django 2.2.28 on 2024-08-14 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0004_add_data_summary_and_item_schema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bsheetitemsv1',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='capitalitemsv1',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='capitalitemsv2',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cflowitemsv1',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cflowitemsv2',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialpositionitemsv2',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incexpitemsv1',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incexpitemsv2',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
    ]
