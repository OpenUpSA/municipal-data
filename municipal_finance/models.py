# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
from __future__ import unicode_literals

from django.db import models


class AgedCreditorFacts(models.Model):
    demarcation_code = models.TextField(blank=True)
    period_code = models.TextField(blank=True)
    item_code = models.ForeignKey('AgedCreditorItems', models.DO_NOTHING, db_column='item_code', blank=True)
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
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'aged_creditor_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'item_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item_code',
                'period_length',
            ),
        )


class AgedCreditorItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True)
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'aged_creditor_items'


class AgedDebtorFacts(models.Model):
    demarcation_code = models.TextField(blank=True)
    period_code = models.TextField(blank=True)
    customer_group_code = models.TextField(blank=True)
    item_code = models.ForeignKey('AgedDebtorItems', models.DO_NOTHING, db_column='item_code', blank=True)
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
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'aged_debtor_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'customer_group_code', 'item_code'),
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


class AgedDebtorItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True)
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'aged_debtor_items'


class AmountType(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True)

    class Meta:
        db_table = 'amount_type'


class AuditOpinionFacts(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.IntegerField()
    opinion_code = models.TextField()
    opinion_label = models.TextField()
    report_url = models.TextField(null=True)

    class Meta:
        db_table = 'audit_opinion_facts'


class AuditOpinions(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.TextField()
    opinion_code = models.TextField()
    opinion_label = models.TextField()

    class Meta:
        db_table = 'audit_opinions'
        unique_together = (('demarcation_code', 'financial_year'),)


class BsheetFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    item_code = models.ForeignKey('BsheetItems', models.DO_NOTHING, db_column='item_code', blank=True)
    amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'bsheet_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'item_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item_code',
                'period_length',
            ),
        )


class BsheetItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True)
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'bsheet_items'


class CapitalFacts(models.Model):
    demarcation_code = models.TextField(blank=True)
    period_code = models.TextField(blank=True)
    function_code = models.ForeignKey('GovernmentFunctions', models.DO_NOTHING, db_column='function_code', blank=True)
    item_code = models.ForeignKey('CapitalItems', models.DO_NOTHING, db_column='item_code', blank=True)
    new_assets = models.BigIntegerField(null=True)
    renewal_of_existing = models.BigIntegerField(null=True)
    total_assets = models.BigIntegerField(null=True)
    repairs_maintenance = models.BigIntegerField(null=True)
    asset_register_summary = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'capital_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'function_code', 'item_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'function_code',
                'item_code',
                'period_length',
            ),
        )


class CapitalItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True)
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'capital_items'


class CflowFacts(models.Model):
    demarcation_code = models.TextField(blank=True)
    period_code = models.TextField(blank=True)
    item_code = models.ForeignKey('CflowItems', models.DO_NOTHING, db_column='item_code', blank=True)
    amount = models.BigIntegerField(null=True)
    amount_type_code = models.TextField()
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        db_table = 'cflow_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'item_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item_code',
                'period_length',
            ),
        )


class CflowItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True)
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'cflow_items'


class ConditionalGrants(models.Model):
    code = models.TextField(null=True)
    name = models.TextField(null=True)

    class Meta:
        db_table = 'conditional_grants'


class ConditionalGrantsFacts(models.Model):
    demarcation_code = models.TextField(blank=True)
    period_code = models.TextField(blank=True)
    grant_code = models.TextField(blank=True)
    amount = models.BigIntegerField(null=True)
    amount_type_code = models.TextField()
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        db_table = 'conditional_grants_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'grant_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'grant_code',
                'period_length',
            ),
        )


class GovernmentFunctions(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True)
    category_label = models.TextField(blank=True)
    subcategory_label = models.TextField(blank=True)

    class Meta:
        db_table = 'government_functions'


class IncexpFacts(models.Model):
    demarcation_code = models.TextField(blank=True)
    period_code = models.TextField(blank=True)
    function_code = models.TextField(blank=True)
    item_code = models.TextField(blank=True)
    amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'incexp_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'function_code', 'item_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'function_code',
                'item_code',
                'period_length',
            ),
        )


class IncexpItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True)
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'incexp_items'


class MunicipalityStaffContacts(models.Model):
    demarcation_code = models.TextField(blank=True)
    role = models.TextField(blank=True)
    title = models.TextField(null=True)
    name = models.TextField(null=True)
    office_number = models.TextField(null=True)
    fax_number = models.TextField(null=True)
    email_address = models.TextField(null=True)

    class Meta:
        db_table = 'municipality_staff_contacts'


class RepmaintFacts(models.Model):
    demarcation_code = models.TextField(blank=True)
    period_code = models.TextField(blank=True)
    item_code = models.TextField(blank=True)
    amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'repmaint_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'item_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item_code',
                'period_length',
            ),
        )


class RepmaintItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True)
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'repmaint_items'


class UifwexpFacts(models.Model):
    demarcation_code = models.TextField(blank=True)
    financial_year = models.IntegerField(blank=True)
    item_code = models.TextField(blank=True)
    item_label = models.TextField(blank=True)
    amount = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'uifwexp_facts'
        unique_together = (('demarcation_code', 'financial_year', 'item_code'),)


class DemarcationChanges(models.Model):
    date = models.DateField(blank=False, null=False)
    old_code = models.TextField(blank=False, null=False, db_index=True)
    new_code = models.TextField(blank=False, null=False, db_index=True)
    old_code_transition = models.TextField(blank=False, null=False, db_index=True)
    new_code_transition = models.TextField(blank=False, null=False, db_index=True)
