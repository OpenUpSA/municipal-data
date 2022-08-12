from django.contrib.sites.models import Site
from municipal_finance.tests.helpers import BaseSeleniumTestCase
from selenium.webdriver.common.keys import Keys


class SearchTest(BaseSeleniumTestCase):

    def setUp(self):
        super(SearchTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')

    def test_search_enter_keypress(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/"))

        header_search_id = '#municipality-search-2'
        header_toolip_selector = "#w-node-_54ec1572-a19d-23ac-5a5a-133d4c7ba1a7-4c7ba190 > div.nav-search___input.w-form > div.w-form-fail"
        page_search_id = '#Municipality-Search-Hero'
        page_toolip_selector = "body > div.section.section--home-hero > div > div > div > div.home-hero__inner > div.hero-search__wrap > div.hero-search > div.hero-search___input.w-form > div.w-form-fail"

        header_search=selenium.find_element_by_css_selector(header_search_id)
        header_search.send_keys("Cape Agulhas")
        header_search.send_keys(Keys.RETURN)
        error_tooltip = selenium.find_element_by_css_selector(header_toolip_selector)
        assert error_tooltip.value_of_css_property("display") == 'none'
        
        page_search=selenium.find_element_by_css_selector(page_search_id)
        page_search.send_keys("Cape Agulhas")
        page_search.send_keys(Keys.RETURN)
        error_tooltip = selenium.find_element_by_css_selector(page_toolip_selector)
        assert error_tooltip.value_of_css_property("display") == 'none'