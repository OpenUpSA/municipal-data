from django.contrib import admin
from django_q.tasks import async_task
from django.contrib import messages

from . import models
from .forms import UploadForm
from .upload import import_bill_data


@admin.register(models.HouseholdServiceTotal)
class HouseholdServiceBillAdmin(admin.ModelAdmin):
    list_display = (
        "geography",
        "financial_year",
        "budget_phase",
        "household_class",
        "service",
        "total",
    )
    list_filter = ("financial_year", "budget_phase", "household_class")


@admin.register(models.HouseholdBillTotal)
class HouseholdBillTotalAdmin(admin.ModelAdmin):
    list_display = (
        "geography",
        "financial_year",
        "budget_phase",
        "household_class",
        "percent",
        "total",
    )
    list_filter = ("financial_year", "budget_phase", "household_class")
    search_fields = ["geography__name"]


@admin.register(models.DataSetFile)
class DataSetFileAdmin(admin.ModelAdmin):
    list_display = ("csv_file", "file_type")
    form = UploadForm

    def save_model(self, request, obj, form, change):
        messages.add_message(
            request, messages.INFO, "Dataset is currently being processed."
        )
        super().save_model(request, obj, form, change)
        task_id = async_task("household.upload.import_bill_data", obj.id)


@admin.register(models.FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ("budget_year",)


@admin.register(models.HouseholdClass)
class HouseholdClassAdmin(admin.ModelAdmin):
    list_display = ("name", "min_value", "max_value")


admin.site.register(models.BudgetPhase)
admin.site.register(models.HouseholdService)
