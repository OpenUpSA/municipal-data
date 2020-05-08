from django.db import models

from scorecard.models import Geography


class FinancialYear(models.Model):
    budget_year = models.CharField(max_length=10)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.budget_year


class Category(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Indicator(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="indicators"
    )
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    tier = models.CharField(max_length=20)
    reporting = models.CharField(max_length=50)
    measurement = models.CharField(max_length=100)
    alignment = models.CharField(max_length=100)
    formula = models.TextField()
    frequency = models.CharField(max_length=100)
    definition = models.TextField()
    target = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class IndicatorElements(models.Model):
    indicator = models.ForeignKey(
        Indicator, on_delete=models.CASCADE, related_name="elements"
    )
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    definition = models.TextField()

    def __str__(self):
        return self.name


class IndicatorQuarterResult(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE, null=True)
    quarter_one = models.CharField(max_length=20, null=True, verbose_name="Q1")
    quarter_two = models.CharField(max_length=20, null=True, verbose_name="Q2")
    quarter_three = models.CharField(max_length=20, null=True, verbose_name="Q3")
    quarter_four = models.CharField(max_length=20, null=True, verbose_name="Q4")
