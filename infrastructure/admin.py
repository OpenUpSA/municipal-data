from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ("budget_year",)


@admin.register(models.BudgetPhase)
class BudgetPhaseAdmin(admin.ModelAdmin):
    list_display = ("name",)


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


@admin.register(models.Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "budget_phase",
        "financial_year",
        "amount",
    )
