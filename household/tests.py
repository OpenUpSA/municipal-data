from django.test import TestCase
from .models import (
    HouseholdBillTotal,
    HouseholdServiceTotal,
    FinancialYear,
    BudgetPhase,
    HouseholdService,
    HouseholdClass,
)
from scorecard.models import Geography


class HouseholdsTestCase(TestCase):
    def setUp(self):
        FinancialYear.objects.bulk_create(
            [
                FinancialYear(budget_year="2015/16", active=True),
                FinancialYear(budget_year="2016/17", active=True),
                FinancialYear(budget_year="2017/18", active=True),
            ]
        )
        BudgetPhase.objects.bulk_create(
            [BudgetPhase(name="Audited Outcome"), BudgetPhase(name="Original Budget"),]
        )
        HouseholdClass.objects.bulk_create(
            [
                HouseholdClass(name="Middle Income Range"),
                HouseholdClass(name="Indigent HH receiving FBS"),
            ]
        )
        HouseholdService.objects.bulk_create(
            [
                HouseholdService(name="Water"),
                HouseholdService(name="Electricity"),
                HouseholdService(name="Sanitation"),
            ]
        )
        Geography(
            [
                Geography(
                    geo_level="municipality",
                    geo_code="JHB",
                    name="City of Johannesburg",
                    parent_level="province",
                    parent_code="GT",
                    category="A",
                )
            ]
        )

        HouseholdBillTotal.objects.create()

    def test_bill_total(self):
        pass

    def test_service_total(self):
        pass

    def test_average_increase(self):
        pass
