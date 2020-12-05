from django.db import models

from .small_auto_field import SmallAutoField
from .amount_type import AmountTypeV2


class GrantTypes(models.Model):
    name = models.TextField(null=True)

    class Meta:
        abstract = True


class GrantFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        abstract = True


class ConditionalGrantTypesV1(GrantTypes):
    code = models.TextField(primary_key=True)

    class Meta:
        db_table = 'conditional_grant_types'


class ConditionalGrantFactsV1(GrantFacts):
    grant_code = models.TextField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'conditional_grant_facts'
        unique_together = (
            (
                'demarcation_code',
                'period_code',
                'grant_code',
            ),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'grant_code',
                'period_length',
            ),
        )


class GrantTypesV2(GrantTypes):
    id = SmallAutoField(primary_key=True)
    code = models.TextField(unique=True)

    class Meta:
        db_table = 'grant_types_v2'


class GrantFactsV2(GrantFacts):
    grant_type = models.ForeignKey(
        GrantTypesV2,
        models.DO_NOTHING,
    )
    amount_type = models.ForeignKey(
        AmountTypeV2,
        models.DO_NOTHING,
    )

    class Meta:
        db_table = 'grant_facts_v2'
        unique_together = (
            (
                'demarcation_code',
                'period_code',
                'grant_type',
            ),
            (
                'demarcation_code',
                'grant_type',
                'amount_type',
                'financial_period',
                'financial_year',
                'period_length',
            ),
        )
