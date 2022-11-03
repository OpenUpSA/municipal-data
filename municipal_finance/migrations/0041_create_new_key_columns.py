# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion


def populate_items_id(apps, schema_editor):
    item_model = apps.get_model("municipal_finance", "agedcreditoritemsv1")
    db_alias = schema_editor.connection.alias
    items = item_model.objects.using(db_alias).all()
    for i, item in enumerate(items):
        item.id = i + 1
    if items:
        item_model.objects.using(db_alias).bulk_update(items, ["id"])


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0040_auto_20210222_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='agedcreditoritemsv1',
            name='id',
            field=models.IntegerField(null=True),
        ),
        migrations.RunPython(populate_items_id),
        migrations.AlterField(
            model_name='agedcreditorfactsv1',
            name='item_code',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='agedcreditoritemsv1',
            name='code',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='agedcreditoritemsv1',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='agedcreditorfactsv1',
            name='item',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='municipal_finance.AgedCreditorItemsV1'),
            preserve_default=False,
        ),
    ]
