from django.contrib import admin
from django.conf.urls import url
from django.contrib import messages

from . import models
from .forms import UploadQuarterlyFileForm, UploadAnnualFileForm
from django_q.tasks import async_task


@admin.register(models.FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ("budget_year",)


@admin.register(models.BudgetPhase)
class BudgetPhaseAdmin(admin.ModelAdmin):
    list_display = ("name",)


class ExpenditureInline(admin.TabularInline):
    model = models.Expenditure


class QuarterlySpendInline(admin.TabularInline):
    model = models.ProjectQuarterlySpend


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "project_number",
        "project_type",
        "function",
        "ward_location",
        "latitude",
        "longitude",
    )
    search_fields = (
        "geography__name",
        "project_number",
        "function",
        "project_description",
    )
    inlines = [
        ExpenditureInline,
        QuarterlySpendInline,
    ]


@admin.register(models.ProjectQuarterlySpend)
class QuarterlySpendAdmin(admin.ModelAdmin):
    list_display = ("project", "financial_year", "q1", "q2", "q3", "q4")
    list_filter = ["financial_year"]


@admin.register(models.AnnualSpendFile)
class AnnualSpendFileAdmin(admin.ModelAdmin):
    list_display = ("financial_year", "document", "status")
    form = UploadAnnualFileForm

    def save_model(self, request, obj, form, change):
        messages.add_message(
            request, messages.INFO, "Dataset is currently being processed."
        )
        super().save_model(request, obj, form, change)
        task_id = async_task("infrastructure.upload.process_annual_document", obj.id)


@admin.register(models.QuarterlySpendFile)
class QuarterlySpendFileAdmin(admin.ModelAdmin):
    list_display = ("financial_year", "document", "status")
    form = UploadQuarterlyFileForm

    def save_model(self, request, obj, form, change):
        messages.add_message(
            request, messages.INFO, "Dataset is currently being processed."
        )
        super().save_model(request, obj, form, change)
        task_id = async_task("infrastructure.upload.process_quarterly_document", obj.id)
