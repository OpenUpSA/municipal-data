# Create sites and populate initial item data
from django.db import migrations
from django.contrib.sites.models import Site, models
from . import run_data_import
from ..resources import (
    AmountTypeV2Resource,
    GovernmentFunctionsV2Resource,
    BsheetItemsV1Resource,
    CashflowItemsV1Resource,
    AmountTypeV1Resource,
    IncexpItemsV1Resource,
    GovernmentFunctionsV1Resource,
    ConditionalGrantTypesV1Resource,
    GrantTypesV2Resource,
    RepairsMaintenanceItemsV1Resource,
    RepairsMaintenanceItemsV2Resource,
    AgedDebtorItemsV1Resource,
    AgedDebtorItemsV2Resource,
    AgedCreditorItemsV2Resource,
)


def populate_items_id(apps, schema_editor):
    item_model = apps.get_model("municipal_finance", "agedcreditoritemsv1")
    db_alias = schema_editor.connection.alias
    items = item_model.objects.using(db_alias).all()
    for i, item in enumerate(items):
        item.id = i + 1
    item_model.objects.using(db_alias).bulk_update(items, ["id"])


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


class Migration(migrations.Migration):
    dependencies = [
        ("municipal_finance", "0002_django_auto_migrations"),
    ]

    operations = [
        migrations.RunSQL(
            """
        update cflow_facts set
        financial_year = cast(left(period_code, 4) as int),
        amount_type_code = case when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)(M\d{2})?$'
                                    then substr(period_code, 5, 4)
                                when period_code ~ '^\d{4}M\d{2}$'
                                    then 'ACT'
                             end,
        period_length = case when period_code ~ '^\d{4}(ADJB|ORGB)?M\d{2}$'
                                 then 'month'
                             when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)$'
                                 then 'year'
       end,
        financial_period = case when period_code ~ '^\d{4}(ADJB|ORGB)?M\d{2}$'
                                    then cast(right(period_code, 2) as int)
                                when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD)$'
                                    then cast(left(period_code, 4) as int)
        end;
        """
        ),
        migrations.RunSQL(
            """
        update conditional_grant_facts set
        financial_year = cast(left(period_code, 4) as int),
        amount_type_code = case when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)(M\d{2})?$'
                                    then substr(period_code, 5, 4)
                                when period_code ~ '^\d{4}M\d{2}$'
                                    then 'ACT'
        end,
        period_length = case when period_code ~ '^\d{4}M\d{2}$'
                                 then 'month'
                             when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)$'
                                 then 'year'
       end,
        financial_period = case when period_code ~ '^\d{4}M\d{2}$'
                                    then cast(right(period_code, 2) as int)
                                when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)$'
                                    then cast(left(period_code, 4) as int)
        end;
        """
        ),
        run_data_import(AmountTypeV2Resource, "amount_type_v2.csv"),
        run_data_import(
            GovernmentFunctionsV2Resource,
            "government_functions_v2.csv",
        ),
        run_data_import(BsheetItemsV1Resource, "bsheet_items_v1.csv"),
        run_data_import(CashflowItemsV1Resource, "cflow_items_v1.csv"),
        run_data_import(AmountTypeV1Resource, "amount_type_v1.csv"),
        run_data_import(IncexpItemsV1Resource, "incexp_items_v1.csv"),
        run_data_import(GovernmentFunctionsV1Resource, "government_functions_v1.csv"),
        run_data_import(
            ConditionalGrantTypesV1Resource,
            "conditional_grant_types_v1.csv",
        ),
        run_data_import(
            GrantTypesV2Resource,
            "grant_types_v2.csv",
        ),
        run_data_import(
            RepairsMaintenanceItemsV1Resource,
            "repairs_maintenance_items_v1.csv",
        ),
        run_data_import(
            RepairsMaintenanceItemsV2Resource,
            "repairs_maintenance_items_v2.csv",
        ),
        run_data_import(
            AgedDebtorItemsV1Resource,
            "aged_debtor_items_v1.csv",
        ),
        run_data_import(
            AgedDebtorItemsV2Resource,
            "aged_debtor_items_v2.csv",
        ),
        run_data_import(
            AgedCreditorItemsV2Resource,
            "aged_creditor_items_v2.csv",
        ),
        migrations.RunPython(populate_items_id),
        #migrations.AlterField(
        #    model_name='agedcreditoritemsv1',
        #    name='id',
        #    field=models.AutoField(primary_key=True, serialize=False),
        #),
        migrations.RunPython(index_keys),
    ]
