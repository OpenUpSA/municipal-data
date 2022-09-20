from django.db import models

from .small_auto_field import SmallAutoField
from .amount_type import AmountTypeV2


class AgedCreditorItems(models.Model):
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        abstract = True


class AgedCreditorFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    g1_amount = models.BigIntegerField(null=True)
    l1_amount = models.BigIntegerField(null=True)
    l120_amount = models.BigIntegerField(null=True)
    l150_amount = models.BigIntegerField(null=True)
    l180_amount = models.BigIntegerField(null=True)
    l30_amount = models.BigIntegerField(null=True)
    l60_amount = models.BigIntegerField(null=True)
    l90_amount = models.BigIntegerField(null=True)
    total_amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        abstract = True


class AgedCreditorItemsV1(AgedCreditorItems):
    id = models.AutoField(primary_key=True)
    code = models.TextField()

    class Meta:
        db_table = "aged_creditor_items"
        verbose_name_plural = "Aged Creditor Items (v1)"


class AgedCreditorFactsV1(AgedCreditorFacts):
    item = models.ForeignKey(
        AgedCreditorItemsV1,
        models.DO_NOTHING,
    )
    item_code = models.TextField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = "aged_creditor_facts"
        unique_together = (
            (
                "demarcation_code",
                "period_code",
                "item",
            ),
            (
                "amount_type_code",
                "demarcation_code",
                "financial_period",
                "financial_year",
                "period_length",
                "item",
            ),
        )


class AgedCreditorItemsV2(AgedCreditorItems):
    id = SmallAutoField(primary_key=True)
    code = models.TextField(unique=True)

    class Meta:
        db_table = "aged_creditor_items_v2"
        verbose_name_plural = "Aged Creditor Items (v2)"


class AgedCreditorFactsV2(AgedCreditorFacts):
    item = models.ForeignKey(
        AgedCreditorItemsV2,
        models.DO_NOTHING,
    )
    amount_type = models.ForeignKey(
        AmountTypeV2,
        models.DO_NOTHING,
    )

    class Meta:
        db_table = "aged_creditor_facts_v2"
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
