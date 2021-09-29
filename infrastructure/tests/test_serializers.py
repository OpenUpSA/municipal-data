from django.test import TestCase
import json
from infrastructure import models, serializers
from scorecard.models import Geography
from scorecard.serializers import GeographySerializer


class TestSerializers(TestCase):
    @classmethod
    def setUp(cls):
        cls.geography = Geography.objects.create(
            geo_level="X",
            geo_code="geo_code",
            province_name="Western Cape",
            province_code="WC",
            category="A",
        )


    def create_expenditure(
        self, amount, project=None, budget_phase=None, financial_year=None
    ):
        if project is None:
            project = models.Project.objects.create(geography=TestSerializers.geography, latest_implementation_year_id=1)

        if budget_phase is None:
            budget_phase = models.BudgetPhase.objects.create(name="Phase")

        if financial_year is None:
            financial_year = models.FinancialYear.objects.create(
                budget_year="2018/2019"
            )

        expenditure = models.Expenditure.objects.create(
            project=project,
            budget_phase=budget_phase,
            financial_year=financial_year,
            amount=amount,
        )

        return expenditure

    def test_financial_year(self):
        fy = models.FinancialYear.objects.create(budget_year="2018/2019")
        s = serializers.FinancialYearSerializer(fy)
        js = s.data
        self.assertIn("budget_year", js)
        self.assertEquals(js["budget_year"], "2018/2019")

    def test_budget_phase(self):
        phase = models.BudgetPhase.objects.create(name="Adjusted Budget", code="ABC")
        s = serializers.BudgetPhaseSerializer(phase)
        js = s.data
        self.assertIn("name", js)
        self.assertIn("code", js)
        self.assertEquals(js["name"], "Adjusted Budget")
        self.assertEquals(js["code"], "ABC")

    def test_project(self):
        financial_year = models.FinancialYear.objects.create(budget_year="2019/2020")

        fields = {
            "geography": TestSerializers.geography,
            "function": "my function",
            "project_description": "my project description",
            "project_number": "my project number",
            "project_type": "my project type",
            "mtsf_service_outcome": "my mtsf_service_outcome",
            "own_strategic_objectives": "my own_strategic_objectives",
            "asset_class": "my asset_class",
            "asset_subclass": "my asset_subclass",
            "ward_location": "my ward_location",
            "longitude": "100",
            "latitude": "200",
            "latest_implementation_year": financial_year,
        }
        project = models.Project.objects.create(**fields)

        expenditures = [
            self.create_expenditure(100, project=project),
            self.create_expenditure(200, project=project),
        ]

        s = serializers.ProjectSerializer(project)
        js = s.data

        for k, v in js.items():
            self.assertIn(k, js)
            if k == "geography":
                js_geo = GeographySerializer(TestSerializers.geography).data

                self.assertEquals(js_geo, v)
            else:
                self.assertEquals(js[k], v)

        self.assertIn("expenditure", js)
        self.assertEquals(2, len(js["expenditure"]))
        js_expenditure = serializers.ExpenditureSerializer(expenditures[0], context={"request": None}).data
        self.assertEquals(js_expenditure, js["expenditure"][0])

    def test_expenditure(self):
        expenditure = self.create_expenditure(1000)

        s = serializers.ExpenditureSerializer(expenditure, context={"request": None})

        js = s.data
        js_budget_phase = serializers.BudgetPhaseSerializer(
            expenditure.budget_phase, context={"request": None}
        ).data

        js_financial_year = serializers.FinancialYearSerializer(
            expenditure.financial_year, context={"request": None}
        ).data

        self.assertEquals(js["budget_phase"], js_budget_phase)
        self.assertEquals(js["financial_year"], js_financial_year)
        self.assertEquals(float(js["amount"]), float(1000))
