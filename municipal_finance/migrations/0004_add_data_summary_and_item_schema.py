from django.db import migrations
from django_q.tasks import async_task
from . import run_data_import
from ..resources import (
    CapitalTypeV2Resource,
    CapitalItemsV1Resource,
    CashflowItemsV2Resource,
    IncexpItemsV2Resource,
    FinancialPositionItemsV2Resource,
    CapitalItemsV2Resource,
)


def populate_data_summary(apps, schema_editor):
    async_task(
        "municipal_finance.summarise_data.summarise",
        task_name="Summarise Data",
    )


def add_new_schema(apps, schema_editor):
    schema = apps.get_model("municipal_finance", "ItemCodeSchema")
    version = schema(version=0)
    version.save()


class Migration(migrations.Migration):
    dependencies = [
        ("municipal_finance", "0003_add_item_codes"),
    ]

    operations = [
        migrations.RunPython(populate_data_summary),
        migrations.RunPython(add_new_schema),
        run_data_import(CapitalItemsV1Resource, "capital_items_v1.csv"),
        run_data_import(CapitalTypeV2Resource, "capital_type_v2.csv"),
        run_data_import(CashflowItemsV2Resource, "cash_flow_items_v2.csv"),
        run_data_import(
            IncexpItemsV2Resource,
            "income_expenditure_items_v2.csv",
        ),
        run_data_import(
            FinancialPositionItemsV2Resource,
            "financial_position_items_v2.csv",
        ),
        run_data_import(CapitalItemsV2Resource, "capital_items_v2.csv"),
    ]
