from django.contrib.sites.models import Site

from municipal_finance.tests.helpers import BaseSeleniumTestCase


class ScorecardTest(BaseSeleniumTestCase):
    fixtures = ["seeddata", "demo-data", "compiled_profile"]

    def setUp(self):
        super(ScorecardTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')

    def test_scorecard_formula(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        self.wait_until_text_in("#cash-balance", "Cash Balance")
        selenium.find_elements_by_css_selector(".expand-block")[3].click()

        self.wait_until_text_in(".indicator-metric__value", "R13 000")
        self.wait_until_text_in(".indicator-calculation__formula-text", "Cash available at year end")
        self.wait_until_text_in(".is--post-2019-20", "[undefined] item code 4200, Audited Actual")
        self.wait_until_text_in(".is--pre-2019-20", "[Cash Flow] item code 4200, Audited Actual")