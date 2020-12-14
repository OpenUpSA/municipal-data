from django.db import models

from .small_auto_field import SmallAutoField
from .amount_type import AmountTypeV2


class BsheetItems(models.Model):
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        abstract = True


class BsheetItemsV1(BsheetItems):
    code = models.TextField(primary_key=True)

    class Meta:
        db_table = 'bsheet_items'


class BsheetFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        abstract = True


class BsheetFactsV1(BsheetFacts):
    item_code = models.ForeignKey(
        BsheetItemsV1,
        models.DO_NOTHING,
        db_column='item_code',
    )
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'bsheet_facts'
        unique_together = (
            (
                'demarcation_code',
                'period_code',
                'item_code',
            ),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item_code',
                'period_length',
            ),
        )


class FinancialPositionItemsV2(BsheetItems):
    id = SmallAutoField(primary_key=True)
    code = models.TextField(unique=True)

    class Meta:
        db_table = 'financial_position_items_v2'


class FinancialPositionFactsV2(BsheetFacts):
    item = models.ForeignKey(
        FinancialPositionItemsV2,
        models.DO_NOTHING,
    )
    amount_type = models.ForeignKey(
        AmountTypeV2,
        models.DO_NOTHING,
    )

    class Meta:
        db_table = 'financial_position_facts_v2'
        unique_together = (
            (
                'demarcation_code',
                'period_code',
                'item',
            ),
            (
                'amount_type',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item',
                'period_length',
            ),
        )
