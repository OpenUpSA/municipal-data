from django.contrib.sites.models import Site

from municipal_finance.tests.helpers import BaseSeleniumTestCase
from household.models import (
    HouseholdServiceTotal,
    HouseholdBillTotal,
    FinancialYear,
    BudgetPhase,
    HouseholdClass,
    HouseholdService,
)
from scorecard.models import Geography

class HouseholdTest(BaseSeleniumTestCase):
    serialized_rollback = True
    fixtures = ["seeddata", "compiled_profile", "budgetphase", "financialyear", "householdclass", "householdservice"]

    def setUp(self):
        super(HouseholdTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')

    def test_household_indicators(self):
        geography = Geography.objects.get(geo_code="BUF")
        year_2021 = FinancialYear.objects.get(budget_year="2020/21")
        year_2022 = FinancialYear.objects.get(budget_year="2021/22")
        budget_phase = BudgetPhase.objects.get(name="Budget Year")
        class_middle = HouseholdClass.objects.get(name="Middle Income Range")
        class_affordable = HouseholdClass.objects.get(name="Affordable Range")
        class_indigent = HouseholdClass.objects.get(name="Indigent HH receiving FBS")
        service_property = HouseholdService.objects.get(name="Property rates")
        service_electricity = HouseholdService.objects.get(name="Electricity: Basic levy")

        HouseholdBillTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_middle,
            percent=7.83,
            total=3362.41
        )
        HouseholdBillTotal.objects.create(
            geography=geography,
            financial_year=year_2022,
            budget_phase=budget_phase,
            household_class=class_middle,
            percent=7.52,
            total=3830.83
        )
        HouseholdBillTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_affordable,
            percent=7.91,
            total=3489.21
        )
        HouseholdBillTotal.objects.create(
            geography=geography,
            financial_year=year_2022,
            budget_phase=budget_phase,
            household_class=class_affordable,
            percent=7.59,
            total=3912.10
        )
        HouseholdBillTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_indigent,
            percent=8.17,
            total=3567.89
        )
        HouseholdBillTotal.objects.create(
            geography=geography,
            financial_year=year_2022,
            budget_phase=budget_phase,
            household_class=class_indigent,
            percent=7.37,
            total=3730.83
        )

        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_middle,
            service=service_property,
            total=2410
        )
        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_middle,
            service=service_electricity,
            total=2942
        )
        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_affordable,
            service=service_property,
            total=920
        )
        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_affordable,
            service=service_electricity,
            total=2071
        )
        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_indigent,
            service=service_property,
            total=3102
        )
        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_indigent,
            service=service_electricity,
            total=704
        )

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))
        self.wait_until_text_in(".page-heading__title", "Buffalo City")

        income_section = "#income-over-time"
        middle_section = "#middle-income-over-time"
        affordable_section = "#affordable-income-over-time"
        indigent_section = "#indigent-income-over-time"

        self.wait_until_text_in(income_section, "Monthly Total for Income Levels Over Time")
        self.wait_until_text_in(income_section, "Affordable Range")
        self.wait_until_text_in(income_section, "Indigent HH receiving FBS")
        self.wait_until_text_in(income_section, "Middle Income Range")
        self.wait_until_text_in(income_section, "2020/21")
        self.wait_until_text_in(income_section, "2021/22")

        self.wait_until_text_in(middle_section, "Monthly Bills for Middle Income Over Time")
        self.wait_until_text_in(middle_section, "6.97%") # Indicator summary
        self.wait_until_text_in(middle_section, "7.83 %") # Chart label
        self.wait_until_text_in(affordable_section, "Monthly Bills for Affordable Income Over Time")
        self.wait_until_text_in(affordable_section, "6.06%")
        self.wait_until_text_in(affordable_section, "7.91 %")
        self.wait_until_text_in(indigent_section, "Monthly Bills for Indigent Income Over Time")
        self.wait_until_text_in(indigent_section, "2.28%")
        self.wait_until_text_in(indigent_section, "8.17 %")
