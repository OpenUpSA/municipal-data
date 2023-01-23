from django.test import TestCase

from constance import config
from constance.test import override_config


class TestConstance(TestCase):
    fixtures = ["seeddata"]

    def test_default_config(self):
        self.assertEqual(config.CAPITAL_PROJECT_SUMMARY_YEAR, "2019/2020")

    def test_config_change(self):
        with override_config(CAPITAL_PROJECT_SUMMARY_YEAR="2020/2021"):
            self.assertEqual(config.CAPITAL_PROJECT_SUMMARY_YEAR, "2020/2021")
