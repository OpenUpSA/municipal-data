# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AgedCreditorFacts(models.Model):
    demarcation_code = models.TextField(blank=True, null=True)
    period_code = models.TextField(blank=True, null=True)
    item_code = models.ForeignKey('AgedCreditorItems', models.DO_NOTHING, db_column='item_code', blank=True, null=True)
    g1_amount = models.BigIntegerField(blank=True, null=True)
    l1_amount = models.BigIntegerField(blank=True, null=True)
    l120_amount = models.BigIntegerField(blank=True, null=True)
    l150_amount = models.BigIntegerField(blank=True, null=True)
    l180_amount = models.BigIntegerField(blank=True, null=True)
    l30_amount = models.BigIntegerField(blank=True, null=True)
    l60_amount = models.BigIntegerField(blank=True, null=True)
    l90_amount = models.BigIntegerField(blank=True, null=True)
    total_amount = models.BigIntegerField(blank=True, null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'aged_creditor_facts'


class AgedCreditorItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    position_in_return_form = models.IntegerField(blank=True, null=True)
    return_form_structure = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aged_creditor_items'


class AgedDebtorFacts(models.Model):
    demarcation_code = models.TextField(blank=True, null=True)
    period_code = models.TextField(blank=True, null=True)
    customer_group_code = models.TextField(blank=True, null=True)
    item_code = models.ForeignKey('AgedDebtorItems', models.DO_NOTHING, db_column='item_code', blank=True, null=True)
    bad_amount = models.BigIntegerField(blank=True, null=True)
    badi_amount = models.BigIntegerField(blank=True, null=True)
    g1_amount = models.BigIntegerField(blank=True, null=True)
    l1_amount = models.BigIntegerField(blank=True, null=True)
    l120_amount = models.BigIntegerField(blank=True, null=True)
    l150_amount = models.BigIntegerField(blank=True, null=True)
    l180_amount = models.BigIntegerField(blank=True, null=True)
    l30_amount = models.BigIntegerField(blank=True, null=True)
    l60_amount = models.BigIntegerField(blank=True, null=True)
    l90_amount = models.BigIntegerField(blank=True, null=True)
    total_amount = models.BigIntegerField(blank=True, null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'aged_debtor_facts'
        unique_together = (('demarcation_code', 'period_code', 'customer_group_code', 'item_code'),)


class AgedDebtorItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    position_in_return_form = models.IntegerField(blank=True, null=True)
    return_form_structure = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aged_debtor_items'


class AmountType(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amount_type'


class AuditOpinionFacts(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.IntegerField()
    opinion_code = models.TextField()
    opinion_label = models.TextField()
    report_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_opinion_facts'


class AuditOpinions(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.TextField()
    opinion_code = models.TextField()
    opinion_label = models.TextField()

    class Meta:
        managed = False
        db_table = 'audit_opinions'
        unique_together = (('demarcation_code', 'financial_year'),)


class BsheetFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    item_code = models.ForeignKey('BsheetItems', models.DO_NOTHING, db_column='item_code', blank=True, null=True)
    amount = models.BigIntegerField(blank=True, null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'bsheet_facts'
        unique_together = (('demarcation_code', 'period_code', 'item_code'),)


class BsheetItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    position_in_return_form = models.IntegerField(blank=True, null=True)
    return_form_structure = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bsheet_items'


class CapitalFacts(models.Model):
    demarcation_code = models.TextField(blank=True, null=True)
    period_code = models.TextField(blank=True, null=True)
    function_code = models.ForeignKey('GovernmentFunctions', models.DO_NOTHING, db_column='function_code', blank=True, null=True)
    item_code = models.ForeignKey('CapitalItems', models.DO_NOTHING, db_column='item_code', blank=True, null=True)
    new_assets = models.BigIntegerField(blank=True, null=True)
    renewal_of_existing = models.BigIntegerField(blank=True, null=True)
    total_assets = models.BigIntegerField(blank=True, null=True)
    repairs_maintenance = models.BigIntegerField(blank=True, null=True)
    asset_register_summary = models.BigIntegerField(blank=True, null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'capital_facts'
        unique_together = (('demarcation_code', 'period_code', 'function_code', 'item_code'),)


class CapitalItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    position_in_return_form = models.IntegerField(blank=True, null=True)
    return_form_structure = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'capital_items'


class CflowFacts(models.Model):
    demarcation_code = models.TextField(blank=True, null=True)
    period_code = models.TextField(blank=True, null=True)
    item_code = models.ForeignKey('CflowItems', models.DO_NOTHING, db_column='item_code', blank=True, null=True)
    amount = models.BigIntegerField(blank=True, null=True)
    amount_type_code = models.TextField()
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cflow_facts'
        unique_together = (('demarcation_code', 'period_code', 'item_code'),)


class CflowItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    position_in_return_form = models.IntegerField(blank=True, null=True)
    return_form_structure = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cflow_items'


class ConditionalGrants(models.Model):
    code = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conditional_grants'


class ConditionalGrantsFacts(models.Model):
    demarcation_code = models.TextField(blank=True, null=True)
    period_code = models.TextField(blank=True, null=True)
    grant_code = models.TextField(blank=True, null=True)
    amount = models.BigIntegerField(blank=True, null=True)
    amount_type_code = models.TextField()
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'conditional_grants_facts'
        unique_together = (('demarcation_code', 'period_code', 'grant_code'),)


class GovernmentFunctions(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    category_label = models.TextField(blank=True, null=True)
    subcategory_label = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'government_functions'


class IncexpFacts(models.Model):
    demarcation_code = models.TextField(blank=True, null=True)
    period_code = models.TextField(blank=True, null=True)
    function_code = models.TextField(blank=True, null=True)
    item_code = models.TextField(blank=True, null=True)
    amount = models.BigIntegerField(blank=True, null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'incexp_facts'
        unique_together = (('demarcation_code', 'period_code', 'function_code', 'item_code'),)


class IncexpItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    position_in_return_form = models.IntegerField(blank=True, null=True)
    return_form_structure = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'incexp_items'


class MunicipalityStaffContacts(models.Model):
    demarcation_code = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    office_number = models.TextField(blank=True, null=True)
    fax_number = models.TextField(blank=True, null=True)
    email_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'municipality_staff_contacts'


class RepmaintFacts(models.Model):
    demarcation_code = models.TextField(blank=True, null=True)
    period_code = models.TextField(blank=True, null=True)
    item_code = models.TextField(blank=True, null=True)
    amount = models.BigIntegerField(blank=True, null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'repmaint_facts'
        unique_together = (('demarcation_code', 'period_code', 'item_code'),)


class RepmaintItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField(blank=True, null=True)
    position_in_return_form = models.IntegerField(blank=True, null=True)
    return_form_structure = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repmaint_items'


class ScorecardGeography(models.Model):
    geo_level = models.CharField(max_length=15)
    geo_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    long_name = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    square_kms = models.FloatField(blank=True, null=True)
    parent_level = models.CharField(max_length=15, blank=True, null=True)
    parent_code = models.CharField(max_length=10, blank=True, null=True)
    province_name = models.CharField(max_length=100)
    province_code = models.CharField(max_length=5)
    category = models.CharField(max_length=2)
    postal_address_1 = models.TextField(blank=True, null=True)
    postal_address_2 = models.TextField(blank=True, null=True)
    postal_address_3 = models.TextField(blank=True, null=True)
    street_address_1 = models.TextField(blank=True, null=True)
    street_address_2 = models.TextField(blank=True, null=True)
    street_address_4 = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    fax_number = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    street_address_3 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scorecard_geography'
        unique_together = (('geo_level', 'geo_code'),)


class UifwexpFacts(models.Model):
    demarcation_code = models.TextField(blank=True, null=True)
    financial_year = models.IntegerField(blank=True, null=True)
    item_code = models.TextField(blank=True, null=True)
    item_label = models.TextField(blank=True, null=True)
    amount = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uifwexp_facts'
        unique_together = (('demarcation_code', 'financial_year', 'item_code'),)
