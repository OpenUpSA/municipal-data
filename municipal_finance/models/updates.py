
from django.db import models

from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible


@deconstructible
class UpdateFilePath(object):

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        timestamp = instance.datetime.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{instance.file_path}{timestamp}.{ext}"
        return filename


class BaseUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    datetime = models.DateTimeField(auto_now_add=True)
    deleted = models.BigIntegerField(null=True)
    inserted = models.BigIntegerField(null=True)
    file = models.FileField(
        upload_to=UpdateFilePath(),
        max_length=255,
    )

    class Meta:
        abstract = True


class MunicipalStaffContactsUpdate(BaseUpdate):
    file_path = "updates/municipal_staff_contacts/"

    class Meta:
        db_table = "municipal_staff_contacts_update"


class IncomeExpenditureV2Update(BaseUpdate):
    file_path = "updates/income_expenditure_v2/"

    class Meta:
        db_table = "income_expenditure_v2_update"


class CashFlowV2Update(BaseUpdate):
    file_path = "updates/cash_flow_v2/"

    class Meta:
        db_table = "cash_flow_v2_update"


class RepairsMaintenanceV2Update(BaseUpdate):
    file_path = "updates/repairs_maintenance_v2/"

    class Meta:
        db_table = "repairs_maintenance_v2_update"


class AgedDebtorFactsV2Update(BaseUpdate):
    file_path = "updates/aged_debtors_v2/"

    class Meta:
        db_table = "aged_debtors_facts_v2_update"


class AgedCreditorFactsV2Update(BaseUpdate):
    file_path = "updates/aged_creditors_v2/"

    class Meta:
        db_table = "aged_creditors_facts_v2_update"


class CapitalFactsV2Update(BaseUpdate):
    file_path = "updates/capital_facts_v2/"

    class Meta:
        db_table = "capital_facts_v2_update"


class GrantFactsV2Update(BaseUpdate):
    file_path = "updates/grant_facts_v2/"

    class Meta:
        db_table = "grant_facts_v2_update"


class FinancialPositionFactsV2Update(BaseUpdate):
    file_path = "updates/financial_position_facts_v2/"

    class Meta:
        db_table = "financial_position_facts_v2_update"


class UIFWExpenseFactsUpdate(BaseUpdate):
    file_path = "updates/uifw_expense_facts/"

    class Meta:
        db_table = "uifw_expense_facts_update"


class AuditOpinionFactsUpdate(BaseUpdate):
    file_path = "updates/audit_opinion_facts/"

    class Meta:
        db_table = "audit_opinion_facts_update"
