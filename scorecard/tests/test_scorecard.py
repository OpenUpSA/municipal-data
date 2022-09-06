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
        element = selenium.find_element_by_css_selector('#cash-balance')
        self.assertIn('R1 823 063 888', element.text)
        expected_formula = '[Cash Flow] item code 4200, Audited Actual'
        self.assertIn(expected_formula, element.get_attribute("innerHTML"))

        # Cash Coverage
        element = selenium.find_element_by_css_selector('#cash-coverage')
        self.assertIn('3.2 month', element.text)
        expected_formula = '[Cash Flow] item code 4200, Audited Actual / ( [Income & Expenditure] item code 4600, Adjusted Budget / 12 )'
        self.assertIn(expected_formula, self.html_to_text(element.get_attribute("innerHTML")))

        # Spending of Operating Budget
        element = selenium.find_element_by_css_selector('#operating-budget')
        self.assertIn('3.7% underspent', element.text)
        expected_formula = '( ( [Income & Expenditure] item code 4600, Audited Actual - [Income & Expenditure] item code 4600, Adjusted Budget ) / [Income & Expenditure] item code 4600, Adjusted Budget ) * 100'
        self.assertIn(expected_formula, self.html_to_text(element.get_attribute("innerHTML")))

        # Spending of Capital Budget
        element = selenium.find_element_by_css_selector('#capital-budget')
        self.assertIn('88.4% underspent', element.text)
        expected_formula = '( ( [Capital] item code 4100, Audited Actual - [Capital] item code 4100, Adjusted Budget ) / [Capital] item code 4100, Adjusted Budget ) * 100'
        self.assertIn(expected_formula, self.html_to_text(element.get_attribute("innerHTML")))

        # Spending on Repairs and Maintenance
        element = selenium.find_element_by_css_selector('#repairs-maintenance')
        self.assertIn('1.9%', element.text)
        expected_formula = '( [Capital] item code 4100, Audited Actual / ( [Balance Sheet] item code 1300, Audited Actual + [Balance Sheet] item code 1401, Audited Actual ) ) * 100'
        self.assertIn(expected_formula, self.html_to_text(element.get_attribute("innerHTML")))

        # Fruitless and Wasteful Expenditure
        element = selenium.find_element_by_css_selector('#wasteful-expenditure')
        expected_formula = '( [Unauthorised, Irregular, Fruitless and Wasteful Expenditure] item code irregular, fruitless, unauthorised / [Income & Expenditure] item code 4600, Audited Actual ) * 100'
        self.assertIn(expected_formula, self.html_to_text(element.get_attribute("innerHTML")))

        # Current Ratio
        element = selenium.find_element_by_css_selector('#current-ratio')
        self.assertIn('1.18', element.text)
        expected_formula = '[Balance Sheet] item code 2150, Audited Actual / [Balance Sheet] item code 1600, Audited Actual'
        self.assertIn(expected_formula, self.html_to_text(element.get_attribute("innerHTML")))

        # Liquidity Ratio
        element = selenium.find_element_by_css_selector('#liquidity-ratio')
        self.assertIn('0.19', element.text)
        expected_formula = '[Balance Sheet] item code 1800, 2200, Audited Actual / [Balance Sheet] item code 1600, Audited Actual'
        self.assertIn(expected_formula, self.html_to_text(element.get_attribute("innerHTML")))

        # Current Debtors Collection Rate
        element = selenium.find_element_by_css_selector('#collection-rate')
        self.assertIn('0.7%', element.text)
        expected_formula = '( [Cash Flow] item code 3010, 3030, 3040, 3050, 3060, 3070, 3100, Audited Actual / [Income & Expenditure] item code 0200, 0400, 1000, Audited Actual ) * 100'
        self.assertIn(expected_formula, self.html_to_text(element.get_attribute("innerHTML")))

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

    def test_grants_section(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        element = selenium.find_element_by_css_selector('#income-summary').text
        self.assertIn('2018-2019 Audited actual', element)
        self.assertIn('R6 040 712 322', element)

        element = selenium.find_element_by_css_selector('#types-of-transfers').text
        self.assertIn('2019-2020 Original budget', element)
        self.assertIn('R2 050 190 000', element)
        element = selenium.find_element_by_css_selector('#types-of-transfers .dropdown').get_attribute("innerHTML")
        self.assertIn('2018-2019 Original budget', element)
        self.assertIn('2019-2020 Original budget', element)

        element = selenium.find_element_by_css_selector('#equitable-share').text
        self.assertIn('2019-2020 Original budget', element)
        self.assertIn('R847 431 000', element)
        element = selenium.find_element_by_css_selector('#equitable-share .dropdown').get_attribute("innerHTML")
        self.assertIn('2018-2019 Original budget', element)
        self.assertIn('2019-2020 Original budget', element)

        element = selenium.find_element_by_css_selector('#national-conditional-grants').text
        self.assertIn('2019-2020 Allocations', element)
        self.assertIn('R285 942 000', element)

        element = selenium.find_element_by_css_selector('#provincial-transfers').text
        self.assertIn('2019-2020 Original budget', element)
        self.assertIn('R87 171 000', element)

    def test_grants_dropdown_select(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        element = selenium.find_element_by_css_selector('#types-of-transfers').text
        self.assertIn('2019-2020 Original budget', element)
        self.assertIn('R2 050 190 000', element)

        dropdown = selenium.find_elements_by_css_selector('#types-of-transfers .dropdown a')
        dropdown[1].click()
        element = selenium.find_element_by_css_selector('#types-of-transfers').text
        self.assertIn('R183 861 100', element)
