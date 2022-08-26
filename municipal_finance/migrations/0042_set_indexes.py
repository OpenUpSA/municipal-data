# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


def index_keys(apps, schema_editor):
    item_model = apps.get_model("municipal_finance", "agedcreditoritemsv1")
    fact_model = apps.get_model("municipal_finance", "agedcreditorfactsv1")
    db_alias = schema_editor.connection.alias
    items = item_model.objects.using(db_alias).all()
    facts = fact_model.objects.using(db_alias).all()
    for i, fact in enumerate(facts):
        item = items.get(code=fact.item_code)
        fact.item_id = item.id
    fact_model.objects.using(db_alias).bulk_update(facts, ["item_id"])

def drop_fact_item_codes(apps, schema_editor):
    print("drop_fact_item_codes")
    

class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0041_create_new_key_columns'),
    ]

    operations = [
        migrations.RunPython(index_keys),
        migrations.RunPython(drop_fact_item_codes),
    ]