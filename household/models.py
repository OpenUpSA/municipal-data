from django.db import models
from scorecard.models import Geography

class FinancialYear(models.Model):
    budget_year = models.CharField(max_length=10)

    def __str__(self):
        return self.budget_year


class BudgetPhase(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class HouseholdClass(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HouseholdService(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class HouseholdBill(models.Model):
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    budget_phase = models.ForeignKey(BudgetPhase, on_delete=models.CASCADE)
    household_class = models.ForeignKey(HouseholdClass, on_delete=models.CASCADE)
    service = models.ForeignKey(HouseholdService, on_delete=models.CASCADE)
    service_vat = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        unique_together = ('financial_year', 'budget_phase', 'household_class', 'service', 'total')


class HouseholdIncrease(models.Model):
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    budget_phase = models.ForeignKey(BudgetPhase, on_delete=models.CASCADE)
    household_class = models.ForeignKey(HouseholdClass, on_delete=models.CASCADE)
    percent = models.FloatField()
