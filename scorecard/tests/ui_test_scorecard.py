from django.contrib.sites.models import Site
from django.core.management import call_command

from municipal_finance.tests.helpers import BaseSeleniumTestCase


class ScorecardTest(BaseSeleniumTestCase):
    fixtures = ["seeddata", "demo-data", "compiled_profile"]

    def setUp(self):
        super(ScorecardTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')

    def test_formulas(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        self.wait_until_text_in(".page-heading__title", "Buffalo City")
        self.wait_until_text_in("#cash-balance", "Cash Balance")
        self.wait_until_text_in(".indicator-detail", "Cash balance at the end of the financial year.")
        self.wait_until_text_in(".layout-grid__col--border-right", "Show calculation")

        selenium.find_elements_by_css_selector(".expand-block")[3].click()

        self.wait_until_text_in(".indicator-metric__value", "R1 823 063 888")
        self.wait_until_text_in(".indicator-calculation__formula-text", "Cash available at year end")
        self.wait_until_text_in(".is--post-2019-20", "item code 0430, Audited Actual")
        self.wait_until_text_in(".is--pre-2019-20", "item code 4200, Audited Actual")

    def test_data_explorer_links(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        selenium.find_elements_by_css_selector(".expand-block")[3].click()

        element = selenium.find_element_by_css_selector('.is--post-2019-20 a').get_attribute("href")
        assert element == "http://portal:8002/table/cflow_v2/?municipalities=BUF&year=2019&items=4200&amountType=AUDA"

        element = selenium.find_element_by_css_selector('.is--pre-2019-20 a').get_attribute("href")
        assert element == "http://portal:8002/table/cflow/?municipalities=BUF&year=2019&items=4200&amountType=AUDA"