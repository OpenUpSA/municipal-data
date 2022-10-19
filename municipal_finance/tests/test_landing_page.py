from django.contrib.sites.models import Site
from municipal_finance.tests.helpers import BaseSeleniumTestCase
import os

class TestLandingPage(BaseSeleniumTestCase):
    serialized_rollback = True
    portal_address = os.getenv('DATA_PORTAL_URL')

    def setUp(self):
        super(TestLandingPage, self).setUp()
        Site.objects.filter(id=3).update(domain='https://municipaldata.treasury.gov.za/', name='API')

    def test_accordion(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.portal_address, "/"))
        self.wait_until_text_in("#header h1", "Municipal Finance Data")

        self.wait_until_text_in(".panel-group h4", "Aged Creditor Analysis")
        self.wait_until_text_in(".panel-group .pill", "2 Datasets")

        self.assertFalse(selenium.find_elements_by_css_selector(".cube-list")[0].is_displayed())
        self.click(".group") # Expand accordion
        self.assertTrue(selenium.find_elements_by_css_selector(".cube-list")[0].is_displayed())

        link = selenium.find_element_by_link_text("Documentation")
        link.click()
        self.wait_until_text_in("#cube-aged_creditor", "Aged Creditor Analysis - aged_creditor")

        selenium.get("%s%s" % (self.portal_address, "/"))
        self.click(".group")
        link = selenium.find_element_by_link_text("Explore Data")
        link.click()
        self.wait_until_text_in("#header h1", "Municipal Finance Data Tables")
