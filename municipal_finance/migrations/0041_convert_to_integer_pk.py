from django.db import migrations, models
import municipal_finance.models.small_auto_field
import django.db.models.deletion


def clone_items_table(apps, schema_editor):
    items_original_model = apps.get_model("municipal_finance", "agedcreditoritemsv1")
    items_new_model = apps.get_model("municipal_finance", "AgedCreditorItemsV1Migrate")
    db_alias = schema_editor.connection.alias
    items_original = items_original_model.objects.using(db_alias).all()

    for item in items_original:
        items_new_model.objects.using(db_alias).create(label=item.label, position_in_return_form=item.position_in_return_form, 
            return_form_structure=item.return_form_structure, composition=item.composition, code=item.code)

def link_new_indexes(apps, schema_editor):
    items_model = apps.get_model("municipal_finance", "AgedCreditorItemsV1Migrate")
    facts_model = apps.get_model("municipal_finance", "AgedCreditorFactsV1")
    db_alias = schema_editor.connection.alias
    facts = facts_model.objects.using(db_alias).all()

    for fact in facts:
        item = items_model.objects.using(db_alias).get(code=fact.item_code.code)
        fact.item=item
        fact.save()

class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0040_auto_20210222_0541'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='agedcreditoritemsv1',
            table='aged_creditor_items_v1',
        ),
        migrations.CreateModel(
            name='AgedCreditorItemsV1Migrate',
            fields=[
                ('label', models.TextField()),
                ('position_in_return_form', models.IntegerField(null=True)),
                ('return_form_structure', models.TextField(null=True)),
                ('composition', models.TextField(null=True)),
                ('id', municipal_finance.models.small_auto_field.SmallAutoField(primary_key=True, serialize=False)),
                ('code', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Aged Creditor Items (v1)',
                'db_table': 'aged_creditor_items',
            },
        ),
        migrations.AddField(
            model_name='agedcreditorfactsv1',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='municipal_finance.AgedCreditorItemsV1Migrate'),
            preserve_default=False,
        ),
        migrations.RunPython(clone_items_table),
        migrations.RunPython(link_new_indexes),
    ]