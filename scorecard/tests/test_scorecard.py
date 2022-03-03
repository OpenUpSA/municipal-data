from django.contrib.sites.models import Site

from municipal_finance.tests.helpers import BaseSeleniumTestCase


class ScorecardTest(BaseSeleniumTestCase):
    serialized_rollback = True
    fixtures = ["seeddata", "compiled_profile"]

    def setUp(self):
        super(ScorecardTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')

    def test_calculation_element(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        self.wait_until_text_in(".page-heading__title", "Buffalo City")
        self.wait_until_text_in("#cash-balance", "Cash Balance")
        self.wait_until_text_in(".indicator-detail", "Cash balance at the end of the financial year.")
        self.wait_until_text_in(".layout-grid__col--border-right", "Show calculation")

        selenium.find_elements_by_css_selector(".expand-block")[3].click()

        self.wait_until_text_in(".indicator-metric__value", "R1 823 063 888")

        element = selenium.find_elements_by_css_selector('.expand-block__content_inner')[3].get_attribute("innerHTML")
        self.assertIn('[Cash Flow] item code 4200, Audited Actual', element)
        self.assertIn('http://portal:8002/', element)
