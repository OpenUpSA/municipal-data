from django.db import models

from .small_auto_field import SmallAutoField
from .government_functions import (
    GovernmentFunctionsV1,
    GovernmentFunctionsV2,
)
from .amount_type import AmountTypeV2


class CapitalItems(models.Model):
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        abstract = True


class CapitalFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        abstract = True


class CapitalItemsV1(CapitalItems):
    code = models.TextField(primary_key=True)

    class Meta:
        db_table = "capital_items"
        verbose_name_plural = "Capital Items (v1)"


class CapitalFactsV1(CapitalFacts):
    amount_type_code = models.TextField()
    function_code = models.ForeignKey(
        GovernmentFunctionsV1,
        models.DO_NOTHING,
        db_column="function_code"
    )
    item_code = models.ForeignKey(
        CapitalItemsV1,
        models.DO_NOTHING,
        db_column="item_code",
    )
    new_assets = models.BigIntegerField(null=True)
    renewal_of_existing = models.BigIntegerField(null=True)
    total_assets = models.BigIntegerField(null=True)
    repairs_maintenance = models.BigIntegerField(null=True)
    asset_register_summary = models.BigIntegerField(null=True)

    class Meta:
        db_table = "capital_facts"
        unique_together = (
            (
                "demarcation_code",
                "function_code",
                "item_code",
                "period_code",
            ),
            (
                "demarcation_code",
                "function_code",
                "item_code",
                "amount_type_code",
                "financial_period",
                "financial_year",
                "period_length",
            ),
        )


class CapitalTypeV2(models.Model):
    id = SmallAutoField(primary_key=True)
    code = models.TextField(unique=True)
    label = models.TextField(unique=True)

    class Meta:
        db_table = "capital_type_v2"
        verbose_name_plural = "Capital Items (v2)"


class CapitalItemsV2(CapitalItems):
    id = SmallAutoField(primary_key=True)
    code = models.TextField(unique=True)

    class Meta:
        db_table = "capital_items_v2"


class CapitalFactsV2(CapitalFacts):
    id = models.BigAutoField(primary_key=True)
    amount_type = models.ForeignKey(
        AmountTypeV2,
        models.DO_NOTHING,
    )
    function = models.ForeignKey(
        GovernmentFunctionsV2,
        models.DO_NOTHING,
    )
    item = models.ForeignKey(
        CapitalItemsV2,
        models.DO_NOTHING,
    )
    capital_type = models.ForeignKey(
        CapitalTypeV2,
        models.DO_NOTHING,
    )
    amount = models.BigIntegerField(null=True)

    class Meta:
        db_table = "capital_facts_v2"
        unique_together = (
            (
                "demarcation_code",
                "function",
                "item",
                "capital_type",
                "period_code",
            ),
            (
                "demarcation_code",
                "function",
                "item",
                "capital_type",
                "amount_type",
                "financial_period",
                "financial_year",
                "period_length",
            ),
        )
