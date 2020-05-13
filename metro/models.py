from django.db import models
from datetime import datetime
from scorecard.models import Geography
import uuid


class FinancialYearQuerySet(models.QuerySet):
    def active(self):
        active = self.get(active=True)
        return active.budget_year[2:4]


class FinancialYear(models.Model):
    budget_year = models.CharField(max_length=10)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.budget_year

    financial_year = FinancialYearQuerySet.as_manager()
    objects = models.Manager()

    @staticmethod
    def current_quarter():
        QUARTERS = {
            "June July August": "Q1",
            "September October, November": "Q2",
            "December January Febuary": "Q3",
            "March April May": "Q4",
        }
        month = datetime.now().strftime("%B")
        for months in QUARTERS.keys():
            if month in months:
                return QUARTERS[months]


class Category(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    slug = models.SlugField(null=True)

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
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

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
    quarter = FinancialYear.current_quarter()

    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    geography = models.ForeignKey(Geography, on_delete=models.CASCADE, null=True)
    quarter_one = models.CharField(max_length=20, null=True, verbose_name="Q1")
    quarter_two = models.CharField(max_length=20, null=True, verbose_name="Q2")
    quarter_three = models.CharField(max_length=20, null=True, verbose_name="Q3")
    quarter_four = models.CharField(max_length=20, null=True, verbose_name="Q4")

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

        if self.indicator.target is None:
            return False
        if calc >= self.clean_value(self.indicator.target):
            return True
        return False

    def _percentage_target_archived(self, calculation):
        calc = 0
        if self.quarter == "Q1":
            calc = calculation["Q1"]
        elif self.quarter == "Q2":
            calc = (calculation["Q2"]) / 2
        elif self.quarter == "Q3":
            calc = (calculation["Q3"]) / 3
        elif self.quarter == "Q4":
            calc = (calculation["Q4"]) / 4

        if self.indicator.target is None:
            return False
        if calc >= self.clean_value(self.indicator.target):
            return True
        return False

    def target_achived(self):
        """
        Check if targert has been reached
        We cant compare percentage
        """
        calculation = {
            "Q1": self.clean_value(self.quarter_one),
            "Q2": self.clean_value(self.quarter_one)
            + self.clean_value(self.quarter_two),
            "Q3": self.clean_value(self.quarter_one)
            + self.clean_value(self.quarter_two)
            + self.clean_value(self.quarter_three),
            "Q4": self.clean_value(self.quarter_one)
            + self.clean_value(self.quarter_two)
            + self.clean_value(self.quarter_three)
            + self.clean_value(self.quarter_four),
        }
        if (
            "percentage" in self.indicator.name
            or "Percentage" in self.indicator.name
            or "rate" in self.indicator.name
            or "Ratio" in self.indicator.name
            or "Rate" in self.indicator.name
        ):
            self._percentage_target_archived(calculation)
        else:
            self._numbers_target_archived(calculation)

    def current_quarter_value(self):
        quarter_map = {
            "Q1": self.quarter_one,
            "Q2": self.quarter_two,
            "Q3": self.quarter_three,
            "Q4": self.quarter_four,
        }
        return quarter_map[self.quarter]
