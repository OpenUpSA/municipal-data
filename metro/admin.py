from django.contrib import admin
from django.contrib import messages

from . import models


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
        "target",
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
        "quarter_one",
        "quarter_two",
        "quarter_three",
        "quarter_four",
    )


@admin.register(models.FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ("budget_year", "active")

    def save_model(self, request, obj, form, change):
        if change:
            if form.cleaned_data["active"] == False:
                super().save_model(request, obj, form, change)
            else:
                try:
                    active_model = models.FinancialYear.objects.get(active=True)
                except models.FinancialYear.DoesNotExist:
                    super().save_model(request, obj, form, change)
                else:
                    messages.error(request, "A Financial Year Is already active")

        else:
            super().save_model(request, obj, form, change)
