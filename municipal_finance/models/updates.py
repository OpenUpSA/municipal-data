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
    task_id = models.TextField(null=True, editable=False)
    import_report = models.TextField(null=True)
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
        verbose_name = "Municipal Staff Contacts Update"


class IncomeExpenditureV2Update(BaseUpdate):
    file_path = "updates/income_expenditure_v2/"

    class Meta:
        db_table = "income_expenditure_v2_update"
        verbose_name = "Income & Expenditure Facts (v2) Update"


class CashFlowV2Update(BaseUpdate):
    file_path = "updates/cash_flow_v2/"

    class Meta:
        db_table = "cash_flow_v2_update"
        verbose_name = "Cash Flow Facts (v2) Update"


class RepairsMaintenanceV2Update(BaseUpdate):
    file_path = "updates/repairs_maintenance_v2/"

    class Meta:
        db_table = "repairs_maintenance_v2_update"
        verbose_name = "Repairs & Maintenance Facts (v2) Update"


class AgedDebtorFactsV2Update(BaseUpdate):
    file_path = "updates/aged_debtors_v2/"

    class Meta:
        db_table = "aged_debtors_facts_v2_update"
        verbose_name = "Aged Debtors Facts (v2) Update"


class AgedCreditorFactsV2Update(BaseUpdate):
    file_path = "updates/aged_creditors_v2/"

    class Meta:
        db_table = "aged_creditors_facts_v2_update"
        verbose_name = "Aged Creditors Facts (v2) Update"


class CapitalFactsV2Update(BaseUpdate):
    file_path = "updates/capital_facts_v2/"

    class Meta:
        db_table = "capital_facts_v2_update"
        verbose_name = "Capital Facts (v2) Update"


class GrantFactsV2Update(BaseUpdate):
    file_path = "updates/grant_facts_v2/"

    class Meta:
        db_table = "grant_facts_v2_update"
        verbose_name = "Grant Facts (v2) Update"


class FinancialPositionFactsV2Update(BaseUpdate):
    file_path = "updates/financial_position_facts_v2/"

    class Meta:
        db_table = "financial_position_facts_v2_update"
        verbose_name = "Financial Position Facts (v2) Update"


class UIFWExpenseFactsUpdate(BaseUpdate):
    file_path = "updates/uifw_expense_facts/"

    class Meta:
        db_table = "uifw_expense_facts_update"
        verbose_name = "UIFW Expense Facts Update"


class AuditOpinionFactsUpdate(BaseUpdate):
    file_path = "updates/audit_opinion_facts/"

    class Meta:
        db_table = "audit_opinion_facts_update"
        verbose_name = "Audit Opinion Facts Update"


class ItemCodeSchema(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    datetime = models.DateTimeField(auto_now_add=True)
    task_id = models.TextField(null=True, editable=False)
    import_report = models.TextField(null=True)
    file = models.FileField(
        upload_to=UpdateFilePath(),
        max_length=255,
    )

    file_path = "updates/item_code_schema/"

    class Meta:
        db_table = "item_code_schema"
        verbose_name = "Item Code Schema"
