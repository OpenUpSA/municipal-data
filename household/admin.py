from django.contrib import admin
from django_q.tasks import async_task
from django.contrib import messages

from . import models
from .forms import UploadForm
from .upload import import_bill_data

@admin.register(models.HouseholdServiceBill)
class HouseholdBillAdmin(admin.ModelAdmin):
    list_display = ('geography', 'financial_year', 'budget_phase', 'household_class','service', 'total', 'version')


@admin.register(models.HouseholdBillIncrease)
class HouseholdIncreaseAdmin(admin.ModelAdmin):
    list_display = ('geography', 'financial_year', 'budget_phase', 'household_class', 'percent', 'total', 'version')


@admin.register(models.DataSetFile)
class DataSetFileAdmin(admin.ModelAdmin):
    form = UploadForm

    def save_model(self, request, obj, form, change):
        messages.add_message(
            request, messages.INFO, "Dataset is currently being processed."
        )
        super().save_model(request, obj, form, change)
        task_id = async_task(
            "household.upload.import_bill_data", obj.id
        )

admin.site.register(models.FinancialYear)
admin.site.register(models.BudgetPhase)
admin.site.register(models.HouseholdClass)
admin.site.register(models.HouseholdService)
admin.site.register(models.DataSetVersion)
