from django.contrib.sites.models import Site
from django.core.management import call_command

from .. import models
from . import (
    import_data,
)
from .resources import (
    MedianGroupResource,
    RatingCountGroupResource,
)
from municipal_finance.tests.helpers import BaseSeleniumTestCase


fixtures = {
    "geography": {
        "geo_level": "municipality",
        "geo_code": "BUF",
        "name": "Buffalo City",
        "long_name": "Buffalo City, Eastern Cape",
        "square_kms": 2751.69154949282,
        "parent_level": "province",
        "parent_code": "EC",
        "province_name": "Eastern Cape",
        "province_code": "EC",
        "category": "A",
        "miif_category": "A",
        "population": 781026,
        "postal_address_1": "P O BOX 134",
        "postal_address_2": "EAST LONDON",
        "postal_address_3": "5200",
        "street_address_1": "Trust Bank Centre",
        "street_address_2": "C/O Oxford & North Street",
        "street_address_3": "East London",
        "street_address_4": "5200",
        "phone_number": "043 705 2000",
        "fax_number": "043 743 8568",
        "url": "http://www.buffalocity.gov.za",
    }
}

class ScorecardTest(BaseSeleniumTestCase):
    fixtures = ["seeddata", "compiled_profile"]

    def setUp(self):
        super(ScorecardTest, self).setUp()

        self.geography = models.Geography.objects.create(
            **fixtures["geography"])
        import_data(
            MedianGroupResource,
            "views/median_group.csv",
        )
        import_data(
            RatingCountGroupResource,
            "views/rating_count_group.csv",
        )
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

        element = selenium.find_element_by_css_selector('.is--post-2019-20 a').get_attribute("href")
        assert element == "http://portal:8002/table/cflow_v2/?municipalities=BUF&year=2019&items=4200&amountType=AUDA"
        element = selenium.find_element_by_css_selector('.is--pre-2019-20 a').get_attribute("href")
        assert element == "http://portal:8002/table/cflow/?municipalities=BUF&year=2019&items=4200&amountType=AUDA"

        is_displayed = selenium.find_element_by_css_selector('.is--pre-2019-20').is_displayed()
        assert is_displayed == True
        #call_command('loaddata', 'compiled_profile')
        #selenium = self.selenium
        #selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))
        #is_displayed = selenium.find_element_by_css_selector('.is--pre-2019-20').is_displayed()
        #assert is_displayed == False