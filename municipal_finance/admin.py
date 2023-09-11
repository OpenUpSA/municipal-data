from django.contrib import admin
from django_q.tasks import async_task, fetch
from import_export.admin import ImportExportModelAdmin

from .models import (
    MunicipalStaffContactsUpdate,
    IncomeExpenditureV2Update,
    CashFlowV2Update,
    RepairsMaintenanceV2Update,
    AgedDebtorFactsV2Update,
    AgedCreditorFactsV2Update,
    CapitalFactsV2Update,
    GrantFactsV2Update,
    FinancialPositionFactsV2Update,
    UIFWExpenseFactsUpdate,
    AuditOpinionFactsUpdate,
    AgedCreditorItemsV2,
    AgedDebtorItemsV2,
    CflowItemsV2,
    IncexpItemsV2,
    FinancialPositionItemsV2,
    RepairsMaintenanceItemsV2,
    CapitalItemsV2,
    GovernmentFunctionsV2,
    GrantTypesV2,
    CapitalTypeV2,
    DemarcationChanges,
)
from .models import (
    MunicipalStaffContacts,
    AgedCreditorFactsV2,
    UIFWExpenseFacts,
    AuditOpinionFacts,
    IncexpFactsV2,
    CflowFactsV2,
    RepairsMaintenanceFactsV2,
    AgedDebtorFactsV2,
    CapitalFactsV2,
    GrantFactsV2,
    FinancialPositionFactsV2,
)
from .resources import (
    AgedDebtorItemsV2Resource,
    AgedCreditorItemsV2Resource,
    CashflowItemsV2Resource,
    IncexpItemsV2Resource,
    CapitalItemsV2Resource,
    FinancialPositionItemsV2Resource,
    RepairsMaintenanceItemsV2Resource,
    GovernmentFunctionsV2Resource,
    GrantTypesV2Resource,
    CapitalTypeV2Resource,
)

from django import forms
from constance.admin import ConstanceAdmin, ConstanceForm, Config
from infrastructure import models


class CustomConfigForm(ConstanceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        financial_years = models.FinancialYear.objects.all()
        new_choices = ()

        for financial_year in financial_years:
            year_choice = (str(financial_year), str(financial_year))
            new_choices += (year_choice,)

        form_field = forms.ChoiceField(choices=new_choices)
        self.fields["CAPITAL_PROJECT_SUMMARY_YEAR"] = form_field


class ConfigAdmin(ConstanceAdmin):
    change_list_form = CustomConfigForm


admin.site.unregister([Config])
admin.site.register([Config], ConfigAdmin)


class BaseUpdateAdmin(admin.ModelAdmin):
    list_display = ("user", "datetime", "deleted", "inserted", "processing_completed")
    readonly_fields = ("user", "deleted", "inserted", "import_report")

    task_function = None
    task_name = None

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ("user",)
        else:
            return super(BaseUpdateAdmin, self).get_exclude(request, obj)

    def has_change_permission(self, request, obj=None):
        super(BaseUpdateAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        super(BaseUpdateAdmin, self).has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        # Set the user to the current user
        obj.user = request.user
        # Process default save behavior
        super(BaseUpdateAdmin, self).save_model(request, obj, form, change)
        # Queue task
        if not change:
            obj.task_id = async_task(
                self.task_function,
                obj,
                task_name=self.task_name,
                batch_size=10000,
                hook="municipal_finance.summarise_data.summarise_task",
            )
            async_task(
                "municipal_finance.bulk_download.generate_download",
                task_name="Make bulk download",
                cube_model=self.cube_model,
            )
            obj.save()

    def processing_completed(self, obj):
        try:
            task = fetch(obj.task_id)
        except:
            task = None
        if task:
            if task.result:
                error_result = task.result.splitlines()[-1]
                if error_result.startswith("KeyError"):
                    item_code = error_result.split(":")[1]
                    obj.import_report = f"Please check that the following item code exists in the corresponding items table for this upload: {item_code}"
                    obj.save()

            return task.success

    processing_completed.boolean = True
    processing_completed.short_description = "Processing completed"


@admin.register(MunicipalStaffContactsUpdate)
class MunicipalStaffContactsUpdateAdmin(BaseUpdateAdmin):
    cube_model = MunicipalStaffContacts
    task_function = "municipal_finance.update.update_municipal_staff_contacts"
    task_name = "Municipal staff contacts update"


@admin.register(UIFWExpenseFactsUpdate)
class UIFWExpenseFactsUpdateAdmin(BaseUpdateAdmin):
    cube_model = UIFWExpenseFacts
    task_function = "municipal_finance.update.update_uifw_expense_facts"
    task_name = "UIFW Expense Facts update"


@admin.register(AuditOpinionFactsUpdate)
class AuditOpinionFactsUpdateAdmin(BaseUpdateAdmin):
    cube_model = AuditOpinionFacts
    task_function = "municipal_finance.update.update_audit_opinion_facts"
    task_name = "Audit Opinion Facts update"


@admin.register(IncomeExpenditureV2Update)
class IncomeExpenditureV2UpdateAdmin(BaseUpdateAdmin):
    cube_model = IncexpFactsV2
    task_function = "municipal_finance.update.update_income_expenditure_v2"
    task_name = "Income & Expenditure v2 update"


@admin.register(CashFlowV2Update)
class CashFlowV2UpdateAdmin(BaseUpdateAdmin):
    cube_model = CflowFactsV2
    task_function = "municipal_finance.update.update_cash_flow_v2"
    task_name = "Cash flow v2 update"


@admin.register(RepairsMaintenanceV2Update)
class RepairsMaintenanceV2UpdateAdmin(BaseUpdateAdmin):
    cube_model = RepairsMaintenanceFactsV2
    task_function = "municipal_finance.update.update_repairs_maintenance_v2"
    task_name = "Repairs & Maintenance v2 update"


@admin.register(AgedDebtorFactsV2Update)
class AgedDebtorFactsV2UpdateAdmin(BaseUpdateAdmin):
    cube_model = AgedDebtorFactsV2
    task_function = "municipal_finance.update.update_aged_debtor_facts_v2"
    task_name = "Aged Debtor Facts v2 update"


@admin.register(AgedCreditorFactsV2Update)
class AgedCreditorFactsV2UpdateAdmin(BaseUpdateAdmin):
    cube_model = AgedCreditorFactsV2
    task_function = "municipal_finance.update.update_aged_creditor_facts_v2"
    task_name = "Aged Creditor Facts v2 update"


@admin.register(CapitalFactsV2Update)
class CapitalFactsV2UpdateAdmin(BaseUpdateAdmin):
    cube_model = CapitalFactsV2
    task_function = "municipal_finance.update.update_capital_facts_v2"
    task_name = "Capital Facts v2 update"


@admin.register(GrantFactsV2Update)
class GrantFactsV2UpdateAdmin(BaseUpdateAdmin):
    cube_model = GrantFactsV2
    task_function = "municipal_finance.update.update_grant_facts_v2"
    task_name = "Grant Facts v2 update"


@admin.register(FinancialPositionFactsV2Update)
class FinancialPositionFactsV2UpdateAdmin(BaseUpdateAdmin):
    cube_model = FinancialPositionFactsV2
    task_function = "municipal_finance.update.update_financial_position_facts_v2"
    task_name = "FinancialPosition Facts v2 update"


@admin.register(AgedCreditorItemsV2)
class AgedCreditorItemsV2Admin(ImportExportModelAdmin):
    resource_class = AgedCreditorItemsV2Resource
    list_display = (
        "code",
        "label",
    )


@admin.register(AgedDebtorItemsV2)
class AgedDebtorItemsV2Admin(ImportExportModelAdmin):
    resource_class = AgedDebtorItemsV2Resource
    list_display = (
        "code",
        "label",
    )


@admin.register(CflowItemsV2)
class CashFlowItemsV2Admin(ImportExportModelAdmin):
    resource_class = CashflowItemsV2Resource
    list_display = (
        "code",
        "label",
    )


@admin.register(IncexpItemsV2)
class IncexpItemsV2Admin(ImportExportModelAdmin):
    resource_class = IncexpItemsV2Resource
    list_display = (
        "code",
        "label",
    )


@admin.register(FinancialPositionItemsV2)
class FinancialPositionItemsV2Admin(ImportExportModelAdmin):
    resource_class = FinancialPositionItemsV2Resource
    list_display = (
        "code",
        "label",
    )


@admin.register(RepairsMaintenanceItemsV2)
class RepairsMaintenanceItemsV2Admin(ImportExportModelAdmin):
    resource_class = RepairsMaintenanceItemsV2Resource
    list_display = (
        "code",
        "label",
    )


@admin.register(GovernmentFunctionsV2)
class GovernmentFunctionsV2Admin(ImportExportModelAdmin):
    resource_class = GovernmentFunctionsV2Resource
    list_display = (
        "code",
        "label",
    )


@admin.register(GrantTypesV2)
class GrantTypesV2Admin(ImportExportModelAdmin):
    resource_class = GrantTypesV2Resource
    list_display = (
        "code",
        "name",
    )


@admin.register(CapitalTypeV2)
class CapitalTypeV2Admin(ImportExportModelAdmin):
    resource_class = CapitalTypeV2Resource
    list_display = (
        "code",
        "label",
    )


@admin.register(DemarcationChanges)
class DemarcationChangesAdmin(admin.ModelAdmin):
    cube_model = DemarcationChanges
    list_display = (
        "date",
        "old_code",
        "new_code",
        "old_code_transition",
        "new_code_transition",
    )
