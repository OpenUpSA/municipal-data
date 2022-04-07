from django.contrib.sites.models import Site

from municipal_finance.tests.helpers import BaseSeleniumTestCase


class ScorecardTest(BaseSeleniumTestCase):
    serialized_rollback = True
    fixtures = ["seeddata", "compiled_profile"]

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

        # Cash Balance
        element = selenium.find_elements_by_css_selector('.indicator-metric__value')[0].text
        self.assertIn('R1 823 063 888', element)
        element = selenium.find_elements_by_css_selector('.is--pre-2019-20')[0].get_attribute("innerHTML")
        self.assertIn('[Cash Flow] item code 4200, Audited Actual', element)

        # Cash Coverage
        element = selenium.find_elements_by_css_selector('.indicator-metric__value')[1].text
        self.assertIn('3.2 month', element)
        element = selenium.find_elements_by_css_selector('.is--pre-2019-20')[1].get_attribute("innerHTML")
        self.assertIn('[Cash Flow] item code 4200, Audited Actual / ( [Income & Expenditure] item code 4600, Adjusted Budget / 12 )', self.normalise_content(element))

        # Spending of Operating Budget
        element = selenium.find_elements_by_css_selector('.indicator-metric__value')[2].text
        self.assertIn('3.7% underspent', element)
        element = selenium.find_elements_by_css_selector('.is--pre-2019-20')[2].get_attribute("innerHTML")
        self.assertIn('( ( [Income & Expenditure] item code 4600, Audited Actual - [Income & Expenditure] item code 4600, Adjusted Budget ) / [Income & Expenditure] item code 4600, Adjusted Budget ) * 100', self.normalise_content(element))

        # Spending of Capital Budget
        element = selenium.find_elements_by_css_selector('.indicator-metric__value')[3].text
        self.assertIn('88.4% underspent', element)
        element = selenium.find_elements_by_css_selector('.is--pre-2019-20')[3].get_attribute("innerHTML")
        self.assertIn('( ( [Capital] item code 4100, Audited Actual - [Capital] item code 4100, Adjusted Budget ) / [Capital] item code 4100, Adjusted Budget ) * 100', self.normalise_content(element))

        # Spending on Repairs and Maintenance
        element = selenium.find_elements_by_css_selector('.indicator-metric__value')[4].text
        self.assertIn('1.9%', element)
        element = selenium.find_elements_by_css_selector('.is--pre-2019-20')[4].get_attribute("innerHTML")
        self.assertIn('( [Capital] item code 4100, Audited Actual / ( [Balance Sheet] item code 1300, Audited Actual + [Balance Sheet] item code 1401, Audited Actual ) ) * 100', self.normalise_content(element))

        # Fruitless and Wasteful Expenditure
        element = selenium.find_elements_by_css_selector('.is--pre-2019-20')[5].get_attribute("innerHTML")
        self.assertIn('( [Unauthorised, Irregular, Fruitless and Wasteful Expenditure] item code irregular,fruitless,unauthorised / [Income & Expenditure] item code 4600, Audited Actual ) * 100', self.normalise_content(element))

        # Current Ratio
        element = selenium.find_elements_by_css_selector('.indicator-metric__value')[5].text
        self.assertIn('1.18', element)
        element = selenium.find_elements_by_css_selector('.is--pre-2019-20')[6].get_attribute("innerHTML")
        self.assertIn('[Balance Sheet] item code 2150, Audited Actual / [Balance Sheet] item code 1600, Audited Actual', self.normalise_content(element))

        # Liquidity Ratio
        element = selenium.find_elements_by_css_selector('.indicator-metric__value')[6].text
        self.assertIn('0.19', element)
        element = selenium.find_elements_by_css_selector('.is--pre-2019-20')[7].get_attribute("innerHTML")
        self.assertIn('[Balance Sheet] item code 1800,2200, Audited Actual / [Balance Sheet] item code 1600, Audited Actual', self.normalise_content(element))

        # Current Debtors Collection Rate
        element = selenium.find_elements_by_css_selector('.indicator-metric__value')[7].text
        self.assertIn('0.7%', element)
        element = selenium.find_elements_by_css_selector('.is--pre-2019-20')[8].get_attribute("innerHTML")
        self.assertIn('( [Cash Flow] item code 3010,3030,3040,3050,3060,3070,3100, Audited Actual / [Income & Expenditure] item code 0200,0400,1000, Audited Actual ) * 100', self.normalise_content(element))

    def test_data_explorer_links(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))
        self.wait_until_text_in(".page-heading__title", "Buffalo City")
        link_class = '.is--pre-2019-20 a'

        # Cash Balance
        element = selenium.find_elements_by_css_selector(link_class)[0].get_attribute("href")
        self.assertIn('http://portal:8002/table/cflow/?municipalities=BUF&year=2019&items=4200&amountType=AUDA', element)

        # Cash Coverage
        element = selenium.find_elements_by_css_selector(link_class)[1].get_attribute("href")
        self.assertIn('http://portal:8002/table/cflow/?municipalities=BUF&year=2019&items=4200&amountType=AUDA', element)
        element = selenium.find_elements_by_css_selector(link_class)[2].get_attribute("href")
        self.assertIn('http://portal:8002/table/incexp/?municipalities=BUF&year=2019&items=4600&amountType=ADJB', element)

        # Spending of Operating Budget
        element = selenium.find_elements_by_css_selector(link_class)[3].get_attribute("href")
        self.assertIn('http://portal:8002/table/incexp/?municipalities=BUF&year=2019&items=4600&amountType=AUDA', element)
        element = selenium.find_elements_by_css_selector(link_class)[4].get_attribute("href")
        self.assertIn('http://portal:8002/table/incexp/?municipalities=BUF&year=2019&items=4600&amountType=ADJB', element)
        element = selenium.find_elements_by_css_selector(link_class)[5].get_attribute("href")
        self.assertIn('http://portal:8002/table/incexp/?municipalities=BUF&year=2019&items=4600&amountType=ADJB', element)

        # Spending of Capital Budget
        element = selenium.find_elements_by_css_selector(link_class)[6].get_attribute("href")
        self.assertIn('http://portal:8002/table/capital/?municipalities=BUF&year=2019&items=4100&amountType=AUDA', element)
        element = selenium.find_elements_by_css_selector(link_class)[7].get_attribute("href")
        self.assertIn('http://portal:8002/table/capital/?municipalities=BUF&year=2019&items=4100&amountType=ADJB', element)
        element = selenium.find_elements_by_css_selector(link_class)[8].get_attribute("href")
        self.assertIn('http://portal:8002/table/capital/?municipalities=BUF&year=2019&items=4100&amountType=ADJB', element)

        # Spending on Repairs and Maintenance
        element = selenium.find_elements_by_css_selector(link_class)[9].get_attribute("href")
        self.assertIn('http://portal:8002/table/capital/?municipalities=BUF&year=2019&items=4100&amountType=AUDA', element)
        element = selenium.find_elements_by_css_selector(link_class)[10].get_attribute("href")
        self.assertIn('http://portal:8002/table/bsheet/?municipalities=BUF&year=2019&items=1300&amountType=AUDA', element)
        element = selenium.find_elements_by_css_selector(link_class)[11].get_attribute("href")
        self.assertIn('http://portal:8002/table/bsheet/?municipalities=BUF&year=2019&items=1401&amountType=AUDA', element)

        # Fruitless and Wasteful Expenditure
        element = selenium.find_elements_by_css_selector(link_class)[12].get_attribute("href")
        self.assertIn('http://portal:8002/table/uifwexp/?municipalities=BUF&year=2019&items=irregular%2Cfruitless%2Cunauthorised', element)
        element = selenium.find_elements_by_css_selector(link_class)[13].get_attribute("href")
        self.assertIn('http://portal:8002/table/incexp/?municipalities=BUF&year=2019&items=4600&amountType=AUDA', element)

        # Current Ratio
        element = selenium.find_elements_by_css_selector(link_class)[14].get_attribute("href")
        self.assertIn('http://portal:8002/table/bsheet/?municipalities=BUF&year=2019&items=2150&amountType=AUDA', element)
        element = selenium.find_elements_by_css_selector(link_class)[15].get_attribute("href")
        self.assertIn('http://portal:8002/table/bsheet/?municipalities=BUF&year=2019&items=1600&amountType=AUDA', element)

        # Liquidity Ratio
        element = selenium.find_elements_by_css_selector(link_class)[16].get_attribute("href")
        self.assertIn('http://portal:8002/table/bsheet/?municipalities=BUF&year=2019&items=1800%2C2200&amountType=AUDA', element)
        element = selenium.find_elements_by_css_selector(link_class)[17].get_attribute("href")
        self.assertIn('http://portal:8002/table/bsheet/?municipalities=BUF&year=2019&items=1600&amountType=AUDA', element)

        # Current Debtors Collection Rate
        element = selenium.find_elements_by_css_selector(link_class)[18].get_attribute("href")
        self.assertIn('http://portal:8002/table/cflow/?municipalities=BUF&year=2019&items=3010%2C3030%2C3040%2C3050%2C3060%2C3070%2C3100&amountType=AUDA', element)
        element = selenium.find_elements_by_css_selector(link_class)[19].get_attribute("href")
        self.assertIn('http://portal:8002/table/incexp/?municipalities=BUF&year=2019&items=0200%2C0400%2C1000&amountType=AUDA', element)