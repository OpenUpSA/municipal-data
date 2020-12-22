from django.db import models

from .small_auto_field import SmallAutoField
from .amount_type import AmountTypeV2
from .government_functions import GovernmentFunctionsV2


class IncexpItems(models.Model):
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        abstract = True


class IncexpItemsV1(IncexpItems):
    code = models.TextField(primary_key=True)

    class Meta:
        db_table = "incexp_items"
        verbose_name_plural = "Income & Expenditure Items (v1)"


class IncexpItemsV2(IncexpItems):
    id = SmallAutoField(primary_key=True)
    code = models.TextField(unique=True)

    class Meta:
        db_table = "incexp_items_v2"
        verbose_name_plural = "Income & Expenditure Items (v2)"


class IncexpFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        abstract = True


class IncexpFactsV1(IncexpFacts):
    item_code = models.TextField()
    amount_type_code = models.TextField()
    function_code = models.TextField()

    class Meta:
        db_table = "incexp_facts"
        unique_together = (
            (
                "demarcation_code",
                "period_code",
                "function_code",
                "item_code",
            ),
            (
                "amount_type_code",
                "demarcation_code",
                "financial_period",
                "financial_year",
                "function_code",
                "item_code",
                "period_length",
            ),
        )


class IncexpFactsV2(IncexpFacts):
    item = models.ForeignKey(
        IncexpItemsV2,
        models.DO_NOTHING,
    )
    amount_type = models.ForeignKey(
        AmountTypeV2,
        models.DO_NOTHING,
    )
    function = models.ForeignKey(
        GovernmentFunctionsV2,
        models.DO_NOTHING,
    )

    class Meta:
        db_table = "incexp_facts_v2"
        unique_together = (
            (
                "demarcation_code",
                "period_code",
                "function",
                "item",
            ),
            (
                "amount_type",
                "demarcation_code",
                "financial_period",
                "financial_year",
                "function",
                "item",
                "period_length",
            ),
        )
