from django.db import models
from scorecard.models import Geography


class DataSetVersion(models.Model):
    version = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.version}"



class DataSetFile(models.Model):
    csv_file = models.FileField(upload_to='datasets/')
    version = models.ForeignKey(DataSetVersion, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.file_type}-{self.version}'




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



class HouseholdServiceBill(models.Model):
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    budget_phase = models.ForeignKey(BudgetPhase, on_delete=models.CASCADE)
    household_class = models.ForeignKey(HouseholdClass, on_delete=models.CASCADE)
    service = models.ForeignKey(HouseholdService, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    version = models.ForeignKey(DataSetVersion, on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('financial_year', 'budget_phase', 'household_class', 'service', 'total')


    def __str__(self):
        return f'{self.household_class} - {self.service} - {self.total}'
    
class HouseholdBillIncrease(models.Model):
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    budget_phase = models.ForeignKey(BudgetPhase, on_delete=models.CASCADE)
    household_class = models.ForeignKey(HouseholdClass, on_delete=models.CASCADE)
    percent = models.FloatField(null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    version = models.ForeignKey(DataSetVersion, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.household_class} - {self.total}'
