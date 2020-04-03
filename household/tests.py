from django.test import TestCase
from .models import (
    HouseholdBillTotal,
    HouseholdServiceTotal,
    FinancialYear,
    BudgetPhase,
    HouseholdService,
    HouseholdClass,
)


class LoadData(TestCase):
    def setup(self):
        year_2015_2016 = FinancialYear.objects.create(
            budget_year="2015/16", active=True
        )
        year_2016_2017 = FinancialYear.objects.create(
            budget_year="2016/17", active=True
        )
        audited = BudgetPhase.objects.create(name="Audited Outcome")
        original = BudgetPhase.objects.create(name="Original Budget")

        middle = HouseholdClass.objects.create(name="Middle Income Range")
        indigent = HouseholdClass.objects.create(name="Indigent HH receiving FBS")

        water = HouseholdService.objects.create(name="Water")
        electricity = HouseholdService.objects.create(name="Electricity")


# Create your tests here.
class BillTotalTestCase(TestCase):
    def setup(self):
        pass


class ServiceTotalTestCase(TestCase):
    def setup(self):
        pass
