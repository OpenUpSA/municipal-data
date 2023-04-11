from django.contrib.sites.models import Site

from municipal_finance.tests.helpers import BaseSeleniumTestCase


class ScorecardComparisonTest(BaseSeleniumTestCase):
    serialized_rollback = True
    fixtures = ["seeddata", "compiled_profile"]

    def setUp(self):
        super(ScorecardComparisonTest, self).setUp()
        Site.objects.filter(id=2).update(
            domain="municipalmoney.org.za", name="Scorecard"
        )

    def test_similar_province_hidden(self):
        selenium = self.selenium
        selenium.get(f"{self.live_server_url}/profiles/municipality-BUF-buffalo-city/")

        section_id = "#cash-balance"
        element = selenium.find_element_by_css_selector(
            f"{section_id} .w-dropdown-list a[data-option=similar-same-province]"
        )
        self.click(f"{section_id} .muni-compare .dropdown")
        self.assertTrue(element.is_displayed())

        classes = element.get_attribute("class")
        self.assertIn("dropdown-link--disabled", classes)

        point_enabled = element.value_of_css_property("pointer-events")
        self.assertEquals(point_enabled, "none")
