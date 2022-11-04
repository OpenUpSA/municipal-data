from django.contrib.sites.models import Site

from municipal_finance.tests.helpers import BaseSeleniumTestCase


class ScorecardTest(BaseSeleniumTestCase):
    serialized_rollback = True
    fixtures = ['seeddata', 'compiled_profile']

    def setUp(self):
        super(ScorecardTest, self).setUp()
        Site.objects.filter(id=2).update(
            domain='municipalmoney.org.za', name='Scorecard')

    def test_income_over_time(self):
        selenium = self.selenium
        selenium.get('%s%s' % (self.live_server_url,
                     '/profiles/municipality-BUF-buffalo-city/'))

        section_id = '#income-budget-actual-time'
        element = selenium.find_element_by_css_selector(
            f'{section_id} .municipal-chart .x-axis')
        self.assertIn('2017-2018 2018-2019 2019-2020',
                      element.text.replace('\n', ' '))

    def test_spending_over_time(self):
        selenium = self.selenium
        selenium.get('%s%s' % (self.live_server_url,
                     '/profiles/municipality-BUF-buffalo-city/'))

        section_id = '#spending-budget-actual-time'
        element = selenium.find_element_by_css_selector(
            f'{section_id} .municipal-chart .x-axis')
        self.assertIn('2017-2018 2018-2019 2019-2020',
                      element.text.replace('\n', ' '))
