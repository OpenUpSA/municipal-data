from django.test import TestCase
from django.contrib.sites.models import Site

from municipal_finance.admin import CustomConfigForm
from infrastructure.models import FinancialYear


class TestConstance(TestCase):
    fixtures = ["seeddata", "demo-data"]

    def setUp(self):
        super(TestConstance, self).setUp()
        Site.objects.filter(id=2).update(
            domain="municipalmoney.org.za", name="Scorecard"
        )

    def test_default_config(self):
        form = CustomConfigForm(initial={})
        choices = form.fields["CAPITAL_PROJECT_SUMMARY_YEAR"].choices
        self.assertEqual(choices, [("2019/2020", "2019/2020")])

    def test_additinoal_year(self):
        fy = FinancialYear.objects.create(budget_year="2020/2021")
        form = CustomConfigForm(initial={})
        choices = form.fields["CAPITAL_PROJECT_SUMMARY_YEAR"].choices
        self.assertEqual(
            choices, [("2019/2020", "2019/2020"), ("2020/2021", "2020/2021")]
        )
