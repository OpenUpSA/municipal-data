from django.test import SimpleTestCase
from ...profile_data.indicators import (
    IncomeAdjustments,
)
from collections import defaultdict

class MockAPIData:
    references = defaultdict(lambda: "foobar")
    def __init__(self, results, years):
        self.results = results
        self.years = years


class RevenueSourcesTests(SimpleTestCase):
    maxDiff = None

    def test_v1(self):
        """
        - local and government are summed correctly
        - total is calculated correctly
        - percentages are calculated correctly
        - latest audit year is used, other years ignored
        """
        api_data = MockAPIData(
            {
                "revenue_budget_actual_v1": [
                    {
                        "item.code": "1300",
                        "amount.sum": 200,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "ORGB",
                    },
                    {
                        "item.code": "1300",
                        "amount.sum": 210,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "ADJB",
                    },
                    {
                        "item.code": "1300",
                        "amount.sum": 220,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "AUDA",
                    },
                ],
                "revenue_budget_actual_v2": [],
            },
            [2050, 2049, 2048, 2047]
        )
        expected = {
            2050: [
                {
                    "item": "Fines",
                    "amount": 10,
                    "comparison": "Original to adjusted budget",
                    "percent_changed": 5
                },
                {
                    "item": "Fines",
                    "amount": 20,
                    "comparison": "Original budget to audited outcome",
                    "percent_changed": 10
                },
            ]
        }
        actual = IncomeAdjustments.get_muni_specifics(api_data)
        self.assertEqual(expected, actual)
