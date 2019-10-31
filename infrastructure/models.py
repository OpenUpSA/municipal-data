from django.db import models
from scorecard.models import Geography

class FinancialYear(models.Model):
    budget_year = models.CharField(max_length=10)

    def __str__(self):
        return self.budget_year

class BudgetPhase(models.Model):
    code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

class Project(models.Model):
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE, null=False, related_name="geographies")
    function = models.CharField(max_length=150, blank=True)
    project_description = models.CharField(max_length=255, blank=True)
    project_number = models.CharField(max_length=30, blank=True)
    project_type = models.CharField(max_length=20, blank=True)
    mtsf_service_outcome = models.CharField(max_length=100, blank=True)
    iudf = models.CharField(max_length=100, blank=True)
    own_strategic_objectives = models.CharField(max_length=100, blank=True)
    asset_class = models.CharField(max_length=100, blank=True)
    asset_subclass = models.CharField(max_length=100, blank=True)
    ward_location = models.CharField(max_length=100, blank=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)

    def __str__(self):
        return "%s (%s) - %s" % (self.geography, self.financial_year, self.project_description)

class Expenditure(models.Model):
    project = models.ForeignKey(Project, null=False, related_name="expenditures")
    budget_phase = models.ForeignKey(BudgetPhase, null=False)
    financial_year = models.ForeignKey(FinancialYear, null=False)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return "%s - %s (%s)" % (self.project, self.budget_phase, self.financial_year)
