from municipal_finance.tests.helpers import BaseSeleniumTestCase
from django.test import override_settings

from municipal_finance.models.data_summaries import Summary

import logging
logger = logging.Logger(__name__)

@override_settings(SITE_ID='3')
class TestLandingPage(BaseSeleniumTestCase):
    serialized_rollback = True

    def setUp(self):
        super(TestLandingPage, self).setUp()

    def test_data_summary(self):
        print("_______________________")
        Summary.objects.create(type="years", content='{"count":5, "min":2018, "max":2023}')
        Summary.objects.create(type="municipalities", content='{"count":5, "min":2018, "max":2023}')
        Summary.objects.create(type="facts", content='{"count":2124242}')

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/"))
        logger.debug("__________: %s" % self.selenium.find_element_by_css_selector("body").text)

        self.wait_until_text_in("#header h1", "Municipal Finance Data")

        self.wait_until_text_in("#years h2", "5 years of data")
        self.wait_until_text_in("#years p", "Financial years 2017-2018 to 2022-2023.")

        self.wait_until_text_in("#municipalities h2", "9 municipalities")
        self.wait_until_text_in("#municipalities p", "2 metros, 3 district and 4 local municipalities.")

        self.wait_until_text_in("#facts h2", "2 124 242 million facts")
        self.wait_until_text_in("#facts p", "Budgeted and actual figures for income and expenditure, cash flow and lots more.")
