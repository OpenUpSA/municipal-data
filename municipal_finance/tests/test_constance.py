from django.test import TestCase
from django.contrib.sites.models import Site
from constance import config
from constance.test import override_config

from constance.admin import ConstanceForm


class TestConstance(TestCase):
    fixtures = ["seeddata", "demo-data"]

    def setUp(self):
        super(TestConstance, self).setUp()
        Site.objects.filter(id=2).update(
            domain="municipalmoney.org.za", name="Scorecard"
        )

    def test_default_config(self):
        form = ConstanceForm()

        self.assertEqual(config.CAPITAL_PROJECT_SUMMARY_YEAR, "2019/2020")

    def test_config_change(self):
        with override_config(CAPITAL_PROJECT_SUMMARY_YEAR="2020/2021"):
            self.assertEqual(config.CAPITAL_PROJECT_SUMMARY_YEAR, "2020/2021")
