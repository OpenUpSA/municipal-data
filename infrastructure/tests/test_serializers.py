from django.test import TestCase
import json
from infrastructure import utils
from infrastructure import models, serializers
from scorecard.models import Geography

class TestSerializers(TestCase):

    @classmethod
    def setUp(cls):
        cls.geography = Geography.objects.create(geo_level="X", geo_code="geo_code", province_name="Western Cape", province_code="WC", category="A")

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

        }
        project = models.Project.objects.create(**fields)

        s = serializers.ProjectSerializer(project)
        js = s.data

        for k, v in js.items():
            self.assertIn(k, js)
            if k == "geography":
                self.assertEquals(TestSerializers.geography.id, v)
            else:
                self.assertEquals(js[k], v)
        

    def test_expenditure(self):
        project = models.Project.objects.create(geography=TestSerializers.geography)
        budget_phase = models.BudgetPhase.objects.create(name="Phase")
        financial_year = models.FinancialYear.objects.create(budget_year="2018/2019")

        expenditure = models.Expenditure.objects.create(
            project=project, budget_phase=budget_phase,
            financial_year=financial_year, amount=1000
        )

        s = serializers.ExpenditureSerializer(expenditure)
        js = s.data

        self.assertEquals(js["project"], project.pk)
        self.assertEquals(js["budget_phase"], budget_phase.pk)
        self.assertEquals(js["financial_year"], financial_year.pk)
        self.assertEquals(float(js["amount"]), float(1000))

