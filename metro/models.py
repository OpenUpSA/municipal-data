from django.db import models
from datetime import datetime
from scorecard.models import Geography
import uuid
from django.utils.text import slugify
from enum import Enum


class FinancialYearQuerySet(models.QuerySet):
    def active(self):
        active = self.get(active=True)
        return active.budget_year[2:4]

    def quarter(self):
        year = self.get(active=True)
        return year.quarter


class FinancialYear(models.Model):

    budget_year = models.CharField(max_length=10)
    active = models.BooleanField(default=False)
    quarter = models.CharField(
        max_length=5, null=True, help_text="Current quarter of the financial year"
    )

    def __str__(self):
        return self.budget_year

    financial_year = FinancialYearQuerySet.as_manager()
    objects = models.Manager()


class Category(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    goal = models.CharField(max_length=25, null=True)

    class Meta:
        unique_together = ("code", "name")

    def __str__(self):
        return self.name


class IndicatorElements(models.Model):
    indicator = models.ForeignKey(
        Indicator, on_delete=models.CASCADE, related_name="elements"
    )
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    definition = models.TextField()

    class Meta:
        unique_together = ("code", "name")

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
    target = models.CharField(max_length=20, null=True)

    class Meta:
        unique_together = ("indicator", "financial_year", "geography")

    @staticmethod
    def clean_value(value):
        """
        Clean quarter values so that they can be added together
        """
        if value is None or value == "":
            return 0
        value = value.replace("R", "").replace(",", "").replace("%", "")
        return float(value)

    def _numbers_target_archived(self, calculation):
        calc = 0
        if self.quarter == "Q1":
            calc = calculation["Q1"]
        elif self.quarter == "Q2":
            calc = calculation["Q2"]
        elif self.quarter == "Q3":
            calc = calculation["Q3"]
        elif self.quarter == "Q4":
            calc = calculation["Q4"]

        if self.target is None or self.target == "":
            return False
        if (
            calc >= self.clean_value(self.target)
            and self.indicator.goal == "Higher is better"
        ):
            return True
        elif (
            calc <= self.clean_value(self.target)
            and self.indicator.goal == "Lower is better"
        ):
            return True
        return False

    def _percentage_target_archived(self, calculation):
        calc = 0
        if self.quarter == "Q1":
            calc = calculation["Q1"]
        elif self.quarter == "Q2":
            calc = calculation["Q2"]
        elif self.quarter == "Q3":
            calc = calculation["Q3"]
        elif self.quarter == "Q4":
            calc = calculation["Q4"]

        if self.target is None or self.target == "":
            return False
        if (
            calc >= self.clean_value(self.target)
            and self.indicator.goal == "Higher is better"
        ):
            return True
        elif (
            calc <= self.clean_value(self.target)
            and self.indicator.goal == "Lower is better"
        ):
            return True
        return False

    def target_achived(self):
        """
        Check if targert has been reached
        We cant compare percentages
        """
        self.quarter = FinancialYear.financial_year.quarter()

        calculation = {
            "Q1": self.clean_value(self.quarter_one),
            "Q2": self.clean_value(self.quarter_one),
            "Q3": self.clean_value(self.quarter_one)
            + self.clean_value(self.quarter_two),
            "Q4": self.clean_value(self.quarter_one)
            + self.clean_value(self.quarter_two)
            + self.clean_value(self.quarter_three),
        }
        if (
            "percentage" in self.indicator.name
            or "Percentage" in self.indicator.name
            or "rate" in self.indicator.name
            or "Ratio" in self.indicator.name
            or "Rate" in self.indicator.name
        ):
            return self._percentage_target_archived(calculation)
        else:
            return self._numbers_target_archived(calculation)

    def current_quarter_value(self):
        quarter_map = {
            "Q1": self.quarter_one,
            "Q2": self.quarter_two,
            "Q3": self.quarter_three,
            "Q4": self.quarter_four,
        }
        return quarter_map[self.quarter]


class UpdateFile(models.Model):
    PROGRESS = "In Progress"
    ERROR = "Error Processing File"
    SUCCESS = "File Successfully Processed"

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to="quarterly/")
    quarter = models.CharField(max_length=5, null=True)
    status = models.CharField(max_length=50, null=True)
