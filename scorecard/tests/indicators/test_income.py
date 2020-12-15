from django.test import SimpleTestCase
from ...profile_data.indicators import (
    RevenueSources,
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
                "revenue_breakdown_v1": [
                    {
                        "item.code": "0200",
                        "amount.sum": 100,
                        "financial_year_end.year": 2050
                    },
                    {
                        "item.code": "0300",
                        "amount.sum": 200,
                        "financial_year_end.year": 2050
                    },
                    {
                        "item.code": "1600",
                        "amount.sum": 400,
                        "financial_year_end.year": 2050
                    },
                    {
                        "item.code": "1610",
                        "amount.sum": 500,
                        "financial_year_end.year": 2050
                    },
                    {
                        "item.code": "0200",
                        "amount.sum": 100,
                        "financial_year_end.year": 2049
                    },
                ],
                "revenue_breakdown_v2": [],
            },
            [2050, 2049, 2048, 2047]
        )
        expected = {
            "local": {"amount": 300, "percent": 25.0},
            "government": {"amount": 900, "percent": 75.0},
            "year": 2050,
            "ref": "foobar",
            "total": 1200,
            "rating": "bad",
        }
        actual = RevenueSources.get_muni_specifics(api_data)
        self.assertEqual(expected, actual)


    def test_v1_v2(self):
        """
        - ignore v1 data for the latest audit year since there's v2 data.
        - local and government are summed correctly
        - total is calculated correctly
        - percentages are calculated correctly
        - latest audit year is used, other years ignored
        """
        api_data = MockAPIData(
            {
                "revenue_breakdown_v1": [
                    {
                        "item.code": "0200",
                        "amount.sum": 9999,
                        "financial_year_end.year": 2050
                    },
                ],
                "revenue_breakdown_v2": [
                    {
                        "item.code": "0200",
                        "amount.sum": 100,
                        "financial_year_end.year": 2050
                    },
                    {
                        "item.code": "0300",
                        "amount.sum": 200,
                        "financial_year_end.year": 2050
                    },
                    {
                        "item.code": "1500",
                        "amount.sum": 900,
                        "financial_year_end.year": 2050
                    },
                    {
                        "item.code": "0200",
                        "amount.sum": 100,
                        "financial_year_end.year": 2049
                    },
                ],
            },
            [2050, 2049, 2048, 2047]
        )
        expected = {
            "local": {"amount": 300, "percent": 25.0},
            "government": {"amount": 900, "percent": 75.0},
            "year": 2050,
            "ref": "foobar",
            "total": 1200,
            "rating": "bad",
        }
        actual = RevenueSources.get_muni_specifics(api_data)
        self.assertEqual(expected, actual)
