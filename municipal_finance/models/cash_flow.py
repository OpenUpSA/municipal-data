from django.db import models

from .small_auto_field import SmallAutoField
from .amount_type import AmountTypeV2
from .updates import ItemCodeSchema


class CflowFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        abstract = True


class CflowItems(models.Model):
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        abstract = True


class CflowItemsV1(CflowItems):
    code = models.TextField(primary_key=True)

    class Meta:
        db_table = "cflow_items"
        verbose_name_plural = "Cash Flow Items (v1)"


class CflowFactsV1(CflowFacts):
    item_code = models.ForeignKey(
        CflowItemsV1, models.DO_NOTHING, db_column="item_code"
    )
    amount_type_code = models.TextField()

    class Meta:
        db_table = "cflow_facts"
        unique_together = (
            (
                "demarcation_code",
                "period_code",
                "item_code",
            ),
            (
                "amount_type_code",
                "demarcation_code",
                "financial_period",
                "financial_year",
                "item_code",
                "period_length",
            ),
        )


class CflowItemsV2(CflowItems):
    id = SmallAutoField(primary_key=True)
    code = models.TextField()
    version = models.ForeignKey(
        ItemCodeSchema, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        #unique_together = ("code", "version")
        db_table = "cflow_items_v2"
        verbose_name_plural = "Cash Flow Items (v2)"

    def __str__(self):
        return self.code


class CflowFactsV2(CflowFacts):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(
        CflowItemsV2,
        models.DO_NOTHING,
    )
    amount_type = models.ForeignKey(
        AmountTypeV2,
        models.DO_NOTHING,
    )

    class Meta:
        db_table = "cflow_facts_v2"
        unique_together = (
            (
                "demarcation_code",
                "period_code",
                "item",
            ),
            (
                "amount_type",
                "demarcation_code",
                "financial_period",
                "financial_year",
                "item",
                "period_length",
            ),
        )
