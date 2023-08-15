from municipal_finance.tests.helpers import BaseSeleniumTestCase
from django.test import override_settings

from municipal_finance.models.data_summaries import Summary


@override_settings(
    SITE_ID=3,
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
)
class TestPortalHome(BaseSeleniumTestCase):
    serialized_rollback = True

    def setUp(self):
        super(TestPortalHome, self).setUp()

    def test_data_summary(self):
        Summary.objects.create(
            type="years", content='{"count":5, "min":2018, "max":2023}'
        )
        Summary.objects.create(
            type="municipalities",
            content='{"total":9, "metros":2, "districts":3, "munis":4}',
        )
        Summary.objects.create(type="facts", content='{"count":2124242}')

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/"))

        self.wait_until_text_in("#header h1", "Municipal Finance Data")

        self.wait_until_text_in("#years-summary h2", "5 years of data")
        self.wait_until_text_in("#years-summary p", "Financial years 2017-2018 to 2022-2023.")

        self.wait_until_text_in("#municipalities-summary h2", "9 municipalities")
        self.wait_until_text_in(
            "#municipalities-summary p", "2 metros, 3 district and 4 local municipalities."
        )

        self.wait_until_text_in("#facts-summary h2", "2 124 242 facts")
        self.wait_until_text_in(
            "#facts-summary p",
            "Budgeted and actual figures for income and expenditure, cash flow and lots more.",
        )

    def test_accordion(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/"))

        self.wait_until_text_in("#header h1", "Municipal Finance Data")
        self.wait_until_text_in(".panel-group .group-header", "Aged Creditor Analysis")
        self.wait_until_text_in(".panel-group .pill", "2 Datasets")

        self.assertFalse(
            selenium.find_elements_by_css_selector(".cube-list")[0].is_displayed()
        )
        self.click(".group")  # Expand accordion
        self.assertTrue(
            selenium.find_elements_by_css_selector(".cube-list")[0].is_displayed()
        )

        link = selenium.find_element_by_link_text("Documentation")
        link.click()
        self.wait_until_text_in(
            "#cube-aged_creditor", "Aged Creditor Analysis - aged_creditor"
        )

        selenium.get("%s%s" % (self.live_server_url, "/"))
        self.click(".group")
        link = selenium.find_element_by_link_text("Explore Data")
        link.click()
        self.wait_until_text_in("#header h1", "Municipal Finance Data Tables")
