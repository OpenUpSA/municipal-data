from django.contrib import admin
from django.contrib import messages
from django_q.tasks import async_task

from . import models
from .forms import FinancialYearForm, UpdateFileForm


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


@admin.register(models.Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "tier",
        "measurement",
        "reporting",
        "alignment",
        "frequency",
        "goal",
    )
    list_filter = ("tier", "reporting", "frequency")


@admin.register(models.IndicatorElements)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "definition")


@admin.register(models.IndicatorQuarterResult)
class QuarterResultAdmin(admin.ModelAdmin):
    list_display = (
        "indicator",
        "financial_year",
        "geography",
        "target",
        "quarter_one",
        "quarter_two",
        "quarter_three",
        "quarter_four",
    )
    search_fields = ["geography__geo_code"]


@admin.register(models.FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ("budget_year", "active", "quarter")
    form = FinancialYearForm

    def save_model(self, request, obj, form, change):
        if change:
            if obj.active and form.cleaned_data["active"]:
                super().save_model(request, obj, form, change)
            elif not obj.active and form.cleaned_data["active"]:
                try:
                    active_model = models.FinancialYear.objects.get(active=True)
                except models.FinancialYear.DoesNotExist:
                    super().save_model(request, obj, form, change)
                else:
                    messages.error(request, "A Financial Year Is already active")

        else:
            super().save_model(request, obj, form, change)


@admin.register(models.UpdateFile)
class UpdateFileAdmin(admin.ModelAdmin):
    list_display = ("financial_year", "quarter", "geography", "document", "status")
    form = UpdateFileForm

    def save_model(self, request, obj, form, change):
        messages.add_message(
            request, messages.INFO, "File is currently being processed."
        )
        super().save_model(request, obj, form, change)
        task_id = async_task("metro.upload.process_file", obj.id)
