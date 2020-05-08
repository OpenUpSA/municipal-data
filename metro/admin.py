from django.contrib import admin

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


admin.site.register(models.FinancialYear)
