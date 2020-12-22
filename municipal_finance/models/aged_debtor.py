from django.db import models

from .small_auto_field import SmallAutoField
from .amount_type import AmountTypeV2


class AgedDebtorItems(models.Model):
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        abstract = True


class AgedDebtorFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    customer_group_code = models.TextField()
    bad_amount = models.BigIntegerField(null=True)
    badi_amount = models.BigIntegerField(null=True)
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


class AgedDebtorItemsV1(AgedDebtorItems):
    code = models.TextField(primary_key=True)

    class Meta:
        db_table = 'aged_debtor_items'
        verbose_name_plural = 'Aged Debtor Items (v1)'


class AgedDebtorFactsV1(AgedDebtorFacts):
    item_code = models.ForeignKey(
        AgedDebtorItemsV1,
        models.DO_NOTHING,
        db_column='item_code',
    )
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'aged_debtor_facts'
        unique_together = (
            (
                'demarcation_code',
                'period_code',
                'customer_group_code',
                'item_code',
            ),
            (
                'amount_type_code',
                'customer_group_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item_code',
                'period_length',
            ),
        )


class AgedDebtorItemsV2(AgedDebtorItems):
    id = SmallAutoField(primary_key=True)
    code = models.TextField(unique=True)

    class Meta:
        db_table = 'aged_debtor_items_v2'
        verbose_name_plural = 'Aged Debtor Items (v2)'


class AgedDebtorFactsV2(AgedDebtorFacts):
    item = models.ForeignKey(
        AgedDebtorItemsV2,
        models.DO_NOTHING,
    )
    amount_type = models.ForeignKey(
        AmountTypeV2,
        models.DO_NOTHING,
    )

    class Meta:
        db_table = 'aged_debtor_facts_v2'
        unique_together = (
            (
                'demarcation_code',
                'period_code',
                'customer_group_code',
                'item',
            ),
            (
                'amount_type',
                'customer_group_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item',
                'period_length',
            ),
        )
