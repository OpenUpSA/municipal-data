# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-12-07 08:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import municipal_finance.models.small_auto_field


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0024_delete_auditopinions'),
    ]



    operations = [
        migrations.CreateModel(
            name='GrantFactsV2',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('demarcation_code', models.TextField()),
                ('period_code', models.TextField()),
                ('amount', models.BigIntegerField(null=True)),
                ('financial_year', models.IntegerField()),
                ('period_length', models.TextField()),
                ('financial_period', models.IntegerField()),
                ('amount_type', models.ForeignKey(
                    on_delete=django.db.models.deletion.DO_NOTHING, to='municipal_finance.AmountTypeV2')),
            ],
            options={
                'db_table': 'grant_facts_v2',
            },
        ),
        migrations.CreateModel(
            name='GrantTypesV2',
            fields=[
                ('name', models.TextField(null=True)),
                ('id', municipal_finance.models.small_auto_field.SmallAutoField(
                    primary_key=True, serialize=False)),
                ('code', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'grant_types_v2',
            },
        ),
        migrations.RenameModel(
            old_name='ConditionalGrants',
            new_name='ConditionalGrantTypesV1',
        ),
        migrations.RenameModel(
            old_name='ConditionalGrantsFacts',
            new_name='ConditionalGrantFactsV1',
        ),
        migrations.AlterModelTable(
            name='conditionalgranttypesv1',
            table='conditional_grant_types',
        ),
        migrations.AlterModelTable(
            name='conditionalgrantfactsv1',
            table='conditional_grant_facts',
        ),
        migrations.AlterField(
            model_name='conditionalgranttypesv1',
            name='code',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='grantfactsv2',
            name='grant_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to='municipal_finance.GrantTypesV2'),
        ),
        migrations.AlterUniqueTogether(
            name='grantfactsv2',
            unique_together=set([('demarcation_code', 'period_code', 'grant_type'), ('demarcation_code',
                                                                                     'grant_type', 'amount_type', 'financial_period', 'financial_year', 'period_length')]),
        ),
    ]
