from django.test import SimpleTestCase
from ...profile_data import ApiData
from ...profile_data.indicators import (
    CapitalBudgetSpending,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    CapitalFactsV1Resource,
    CapitalFactsV2Resource,
)


class MockAPIData:
    years = [2040, 2041, 2042, 2043]
    references = {
        "overunder": {
                "title": "test title",
                "url": "http://example.com",
            },
        }

    def __init__(self, results, budget_year):
        self.results = results
        # self.budget_year = budget_year


class CalculatorTests(SimpleTestCase):
    maxDiff = None

    def test_v1(self):
        """ percentages and ratings are calculated correctly """
        api_data = MockAPIData(
            {
                "capital_expenditure_budget_v1": [
                    { "financial_year_end.year": 2040, "total_assets.sum": 3, },
                    { "financial_year_end.year": 2041, "total_assets.sum": 4, },
                    { "financial_year_end.year": 2042, "total_assets.sum": 5, },
                    { "financial_year_end.year": 2043, "total_assets.sum": 6, },
                ],
                "capital_expenditure_actual_v1": [
                    { "financial_year_end.year": 2040, "total_assets.sum": 2, },
                    { "financial_year_end.year": 2041, "total_assets.sum": 8, },
                    { "financial_year_end.year": 2042, "total_assets.sum": 5, },
                    { "financial_year_end.year": 2043, "total_assets.sum": 6.6,
                    },
                ],
                "capital_expenditure_budget_v2": [],
                "capital_expenditure_actual_v2": [],
            },
            2040,
        )
        result = CapitalBudgetSpending.get_muni_specifics(api_data)
        self.assertEqual(
            [{'date': 2040, 'overunder': 'under', 'rating': 'bad', 'result': -33.33},
             {'date': 2041, 'overunder': 'over', 'rating': 'bad', 'result': 100.0},
             {'date': 2042, 'overunder': 'over', 'rating': 'good', 'result': 0.0},
             {'date': 2043, 'overunder': 'over', 'rating': 'ave', 'result': 10.0}],
            result["values"],
        )

    def test_v2(self):
        """ percentages and ratings are calculated correctly """
        api_data = MockAPIData(
            {
                "capital_expenditure_budget_v1": [],
                "capital_expenditure_actual_v1": [],
                "capital_expenditure_budget_v2": [
                    { "financial_year_end.year": 2040, "amount.sum": 3, },
                    { "financial_year_end.year": 2041, "amount.sum": 4, },
                    { "financial_year_end.year": 2042, "amount.sum": 5, },
                    { "financial_year_end.year": 2043, "amount.sum": 6, },
                ],
                "capital_expenditure_actual_v2": [
                    { "financial_year_end.year": 2040, "amount.sum": 2, },
                    { "financial_year_end.year": 2041, "amount.sum": 8, },
                    { "financial_year_end.year": 2042, "amount.sum": 5, },
                    { "financial_year_end.year": 2043, "amount.sum": 6.6, },
                ],
            },
            2040,
        )
        result = CapitalBudgetSpending.get_muni_specifics(api_data)
        self.assertEqual(
            [{'date': 2040, 'overunder': 'under', 'rating': 'bad', 'result': -33.33},
             {'date': 2041, 'overunder': 'over', 'rating': 'bad', 'result': 100.0},
             {'date': 2042, 'overunder': 'over', 'rating': 'good', 'result': 0.0},
             {'date': 2043, 'overunder': 'over', 'rating': 'ave', 'result': 10.0}],
            result["values"],
        )

    def test_v1_v2(self):
        """
        - v2 is used when budget and actual data is available
        - v1 is used when availabel and there isn't both budget and actual
          available from v2
           - 2040 v2 was available for both, v1 was not available
           - 2041 v2 was only available for budget, v1 was available
           - 2042 v2 was only available for actual, v1 was available
           - 2043 neither v1 nor v2 was available
        """
        api_data = MockAPIData(
            {
                "capital_expenditure_budget_v1": [
                    { "financial_year_end.year": 2041, "total_assets.sum": 1, },
                    { "financial_year_end.year": 2042, "total_assets.sum": 1, },
                ],
                "capital_expenditure_actual_v1": [
                    { "financial_year_end.year": 2041, "total_assets.sum": 0.9, },
                    { "financial_year_end.year": 2042, "total_assets.sum": 0.8, },
                ],
                "capital_expenditure_budget_v2": [
                    { "financial_year_end.year": 2040, "amount.sum": 1, },
                    { "financial_year_end.year": 2041, "amount.sum": 0.8, },
                ],
                "capital_expenditure_actual_v2": [
                    { "financial_year_end.year": 2040, "amount.sum": 1, },
                    { "financial_year_end.year": 2042, "amount.sum": 1.2, },
                ],
            },
            2040,
        )
        result = CapitalBudgetSpending.get_muni_specifics(api_data)
        self.assertEqual(
            [{'date': 2040, 'overunder': 'over', 'rating': 'good', 'result': 0.0},
             {'date': 2041, 'overunder': 'under', 'rating': 'ave', 'result': -10.0},
             {'date': 2042, 'overunder': 'under', 'rating': 'bad', 'result': -20.0},
             {'date': 2043, 'overunder': None, 'rating': None, 'result': None}],
            result["values"],
        )



class TestCapitalBudgetSpendingQueryAndCalculator(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'capital_budget_spending/scorecard_geography.csv'
        )
        import_data(
            CapitalFactsV1Resource,
            'capital_budget_spending/capital_facts_v1.csv'
        )
        import_data(
            CapitalFactsV2Resource,
            'capital_budget_spending/capital_facts_v2.csv'
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2019, 2019, 2019, '2019q4')
        api_data.fetch_data([
            "capital_expenditure_budget_v1",
            "capital_expenditure_actual_v1",
            "capital_expenditure_budget_v2",
            "capital_expenditure_actual_v2",
        ])
        # Provide data to indicator
        result = CapitalBudgetSpending.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "%",
                "values": [
                    {
                        "date": 2019,
                        "result": 11.73,
                        "overunder": "over",
                        "rating": "ave"
                    },
                    {
                        "date": 2018,
                        "result": -35.51,
                        "overunder": "under",
                        "rating": "bad"
                    },
                    {
                        "date": 2017,
                        "result": -7.37,
                        "overunder": "under",
                        "rating": "ave"
                    },
                    {
                        "date": 2016,
                        "result": -11.46,
                        "overunder": "under",
                        "rating": "ave"
                    }
                ],
                "ref": {
                    "title": "Over and under spending reports to parliament",
                    "url": "http://mfma.treasury.gov.za/Media_Releases/Reports%20to%20Parliament/Pages/default.aspx"
                },
                "last_year": 2019,
                "formula": {
                    "text": "= ((Actual Capital Expenditure - Budgeted Capital Expenditure) / Budgeted Capital Expenditure) * 100",
                    "actual": [
                        "=",
                        "(",
                        "(",
                        {
                            "cube": "capital",
                            "item_codes": ["4100"],
                            "amount_type": "AUDA",
                        },
                        "-",
                        {
                            "cube": "capital",
                            "item_codes": ["4100"],
                            "amount_type": "ADJB",
                        },
                        ")",
                        "/",
                        {
                            "cube": "capital",
                            "item_codes": ["4100"],
                            "amount_type": "ADJB",
                        },
                        ")",
                        "*",
                        "100",
                    ],
                },
            },
        )
