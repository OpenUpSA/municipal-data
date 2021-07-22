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
        - adjustments calculated correctly for one item in one year
        - this is the absolute minimal functionality of this calculator
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

    def test_v1_two_items(self):
        """
        - two items in results are calculated correctly
        - this is here so that less data can be used in other tests
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
                    {
                        "item.code": "1400",
                        "amount.sum": 300,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "ORGB",
                    },
                    {
                        "item.code": "1400",
                        "amount.sum": 310,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "ADJB",
                    },
                    {
                        "item.code": "1400",
                        "amount.sum": 320,
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
                    "percent_changed": 5.0
                },
                {
                    "item": "Fines",
                    "amount": 20,
                    "comparison": "Original budget to audited outcome",
                    "percent_changed": 10.0
                },
                {
                    "item": "Licenses and Permits",
                    "amount": 10,
                    "comparison": "Original to adjusted budget",
                    "percent_changed": 3.33
                },
                {
                    "item": "Licenses and Permits",
                    "amount": 20,
                    "comparison": "Original budget to audited outcome",
                    "percent_changed": 6.67
                },
            ]
        }
        actual = IncomeAdjustments.get_muni_specifics(api_data)
        self.assertEqual(expected, actual)

    def test_v2(self):
        """
        - v2 data is calculated correctly
        - v2 results replace v1 results even if it's for different item labels
            (i.e. replacement is for the entire set, not per-label)
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
                "revenue_budget_actual_v2": [
                    {
                        "item.code": "0200",
                        "amount.sum": 300,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "ORGB",
                    },
                    {
                        "item.code": "0200",
                        "amount.sum": 310,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "ADJB",
                    },
                    {
                        "item.code": "0200",
                        "amount.sum": 320,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "AUDA",
                    },
                ],
            },
            [2050, 2049, 2048, 2047]
        )
        expected = {
            2050: [
                {
                    "item": "Property rates",
                    "amount": 10,
                    "comparison": "Original to adjusted budget",
                    "percent_changed": 3.33
                },
                {
                    "item": "Property rates",
                    "amount": 20,
                    "comparison": "Original budget to audited outcome",
                    "percent_changed": 6.67
                },
            ]
        }
        actual = IncomeAdjustments.get_muni_specifics(api_data)
        self.assertEqual(expected, actual)

    def test_v2_no_original_budget(self):
        """
        - v2 results don't replace v1 results if original budget is not available
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
                "revenue_budget_actual_v2": [
                    {
                        "item.code": "0200",
                        "amount.sum": 310,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "ADJB",
                    },
                    {
                        "item.code": "0200",
                        "amount.sum": 320,
                        "financial_year_end.year": 2050,
                        "amount_type.code": "AUDA",
                    },
                ],
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
