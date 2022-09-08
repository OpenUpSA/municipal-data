from django.db import models
from django.db.models import Q

from scorecard.models import Geography


class DataSetFile(models.Model):
    csv_file = models.FileField(upload_to="datasets/")
    file_type = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.file_type}"


class FinancialYear(models.Model):

    budget_year = models.CharField(max_length=10)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.budget_year


class BudgetPhase(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HouseholdClass(models.Model):
    name = models.CharField(max_length=100)
    min_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, default=10000)

    def __str__(self):
        return self.name


class HouseholdService(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class HouseholdServiceTotalQuerySet(models.QuerySet):
    def active(self, geo_code):
        return self.filter(
            Q(budget_phase__name="Audited Outcome")
            | Q(budget_phase__name="Adjusted Budget")
            | Q(budget_phase__name="Budget Year"),
            geography__geo_code=geo_code,
            financial_year__active=True,
        )

    def middle(self):
        return self.filter(household_class__name="Middle Income Range").values(
            "financial_year__budget_year",
            "total",
            "service__name",
            "household_class__name",
        )

    def affordable(self):
        return self.filter(household_class__name="Affordable Range").values(
            "financial_year__budget_year",
            "total",
            "service__name",
            "household_class__name",
        )

    def indigent(self):
        return self.filter(household_class__name="Indigent HH receiving FBS").values(
            "financial_year__budget_year",
            "total",
            "service__name",
            "household_class__name",
        )


class HouseholdServiceTotal(models.Model):
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    budget_phase = models.ForeignKey(BudgetPhase, on_delete=models.CASCADE)
    household_class = models.ForeignKey(HouseholdClass, on_delete=models.CASCADE)
    service = models.ForeignKey(HouseholdService, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    objects = models.Manager()
    summary = HouseholdServiceTotalQuerySet.as_manager()

    class Meta:
        unique_together = (
            "geography",
            "financial_year",
            "budget_phase",
            "household_class",
            "service",
            "total",
        )

    def __str__(self):
        return f"{self.household_class} - {self.service} - {self.total}"


class HouseholdBillTotalQuerySet(models.QuerySet):
    def bill_totals(self, geo_code):
        return (
            self.filter(
                Q(budget_phase__name="Audited Outcome")
                | Q(budget_phase__name="Adjusted Budget")
                | Q(budget_phase__name="Budget Year"),
                financial_year__active=True,
                geography__geo_code=geo_code,
            )
            .values(
                "financial_year__budget_year",
                "household_class__name",
                "total",
                "percent",
            )
            .order_by("financial_year__budget_year")
        )


class HouseholdBillTotal(models.Model):
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    budget_phase = models.ForeignKey(BudgetPhase, on_delete=models.CASCADE)
    household_class = models.ForeignKey(HouseholdClass, on_delete=models.CASCADE)
    percent = models.FloatField(null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    objects = models.Manager()
    summary = HouseholdBillTotalQuerySet.as_manager()

    def __str__(self):
        return f"{self.household_class} - {self.total}"

    class Meta:
        unique_together = (
            "geography",
            "financial_year",
            "budget_phase",
            "household_class",
            "total",
        )
