# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from .amount_type import (
    AmountType,
    AmountTypeV2,
)
from .government_functions import (
    GovernmentFunctionsV1,
    GovernmentFunctionsV2,
)
from .cash_flow import (
    CflowItemsV1,
    CflowFactsV1,
    CflowItemsV2,
    CflowFactsV2,
)
from .income_expenditure import (
    IncexpItemsV1,
    IncexpFactsV1,
    IncexpItemsV2,
    IncexpFactsV2,
)
from .financial_position import (
    BsheetItemsV1,
    BsheetFactsV1,
    BsheetItemsV2,
    BsheetFactsV2,
)
from .municipality_profiles_compilation import (
    MunicipalityProfilesCompilation,
)
from .capital import (
    CapitalTypeV2,
    CapitalItemsV1,
    CapitalItemsV2,
    CapitalFactsV1,
    CapitalFactsV2,
)
from .grants import (
    ConditionalGrantTypesV1,
    ConditionalGrantFactsV1,
    GrantTypesV2,
    GrantFactsV2,
)
from .repairs_maintenance import (
    RepairsMaintenanceItemsV1,
    RepairsMaintenanceFactsV1,
    RepairsMaintenanceItemsV2,
    RepairsMaintenanceFactsV2,
)


class AgedCreditorFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    item_code = models.ForeignKey(
        'AgedCreditorItems', models.DO_NOTHING, db_column='item_code')
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
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'aged_creditor_items'


class AgedDebtorFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    customer_group_code = models.TextField()
    item_code = models.ForeignKey(
        'AgedDebtorItems', models.DO_NOTHING, db_column='item_code')
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
            ('demarcation_code', 'period_code',
             'customer_group_code', 'item_code'),
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
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'aged_debtor_items'


class AuditOpinionFacts(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.IntegerField()
    opinion_code = models.TextField()
    opinion_label = models.TextField()
    report_url = models.TextField(null=True)

    class Meta:
        db_table = 'audit_opinion_facts'


class MunicipalityStaffContacts(models.Model):
    id = models.AutoField(primary_key=True)
    demarcation_code = models.TextField()
    role = models.TextField()
    title = models.TextField(null=True)
    name = models.TextField(null=True)
    office_number = models.TextField(null=True)
    fax_number = models.TextField(null=True)
    email_address = models.TextField(null=True)

    class Meta:
        db_table = 'municipality_staff_contacts'
        unique_together = (('demarcation_code', 'role'),)


class MunicipalityStaffContactsUpload(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    datetime = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/contacts/')

    class Meta:
        db_table = 'municipality_staff_contacts_uploads'


class UifwexpFacts(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.IntegerField()
    item_code = models.TextField()
    item_label = models.TextField()
    amount = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'uifwexp_facts'
        unique_together = (
            ('demarcation_code', 'financial_year', 'item_code'),)


class DemarcationChanges(models.Model):
    date = models.DateField(blank=False, null=False)
    old_code = models.TextField(blank=False, null=False, db_index=True)
    new_code = models.TextField(blank=False, null=False, db_index=True)
    old_code_transition = models.TextField(
        blank=False, null=False, db_index=True)
    new_code_transition = models.TextField(
        blank=False, null=False, db_index=True)


class MunicipalityProfile(models.Model):
    demarcation_code = models.CharField(max_length=10, primary_key=True)
    data = JSONField()

    class Meta:
        db_table = 'municipality_profile'


class MedianGroup(models.Model):
    group_id = models.CharField(max_length=10, primary_key=True)
    data = JSONField()


class RatingCountGroup(models.Model):
    group_id = models.CharField(max_length=10, primary_key=True)
    data = JSONField()
