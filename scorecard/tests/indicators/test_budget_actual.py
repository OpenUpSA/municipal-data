from django.test import SimpleTestCase
from ...profile_data.indicators.budget_actual import (
    AdjustmentsCalculator,
    TimeSeriesCalculator,
    combine_versions,
)

class MockAPIData:
    def __init__(self, results, budget_year):
        self.results = results
        self.budget_year = budget_year


class TimeSeriesCalculatorTests(SimpleTestCase):
    maxDiff = None

    def test_combine_v1_v2(self):
        """
        - v2 is used when there's overlap between v1 and v2
        - everything that doesn't overlap must be included
        """

        class TestTimeSeriesCalculator(TimeSeriesCalculator):
            v1_api_data_key = "v1_key"
            v2_api_data_key = "v2_key"

        api_data = MockAPIData(
            {
                "v1_key": [
                    {
                        "amount_type.code": "AUDA",
                        "amount_type.label": "Audited",
                        "financial_year_end.year": 2040,
                        "amount.sum": 123,
                    },
                    {
                        "amount_type.code": "ORGB",
                        "amount_type.label": "Budget",
                        "financial_year_end.year": 2040,
                        "amount.sum": 234,
                    },
                ],
                "v2_key": [
                    {
                        "amount_type.code": "AUDA",
                        "amount_type.label": "Audited",
                        "financial_year_end.year": 2040,
                        "amount.sum": 345,
                    },
                    {
                        "amount_type.code": "ORGB",
                        "amount_type.label": "Budget",
                        "financial_year_end.year": 2041,
                        "amount.sum": 456,
                    },
                ],
            },
            2040,
        )
        result = TestTimeSeriesCalculator.get_muni_specifics(api_data)
        self.assertEqual(
            [
                {
                    "amount_type.code": "ORGB",
                    "budget_phase": "Budget",
                    "financial_year": 2040,
                    "amount": 234,
                },
                {
                    "amount_type.code": "AUDA",
                    "budget_phase": "Audited",
                    "financial_year": 2040,
                    "amount": 345,
                },
                {
                    "amount_type.code": "ORGB",
                    "budget_phase": "Budget",
                    "financial_year": 2041,
                    "amount": 456,
                },
            ],
            result,
        )

    def test_combine_versions(self):
        expected = (
            [
                {
                    "amount_type.code": "ORGB",
                    "amount_type.label": "Budget",
                    "financial_year_end.year": 2040,
                    "amount.sum": 234,
                },
                {
                    "amount_type.code": "AUDA",
                    "amount_type.label": "Audited",
                    "financial_year_end.year": 2040,
                    "amount.sum": 345,
                },
                {
                    "amount_type.code": "ORGB",
                    "amount_type.label": "Budget",
                    "financial_year_end.year": 2041,
                    "amount.sum": 456,
                },
            ],
        )
        actual = (
            combine_versions(
                [
                    {
                        "amount_type.code": "AUDA",
                        "amount_type.label": "Audited",
                        "financial_year_end.year": 2040,
                        "amount.sum": 123,
                    },
                    {
                        "amount_type.code": "ORGB",
                        "amount_type.label": "Budget",
                        "financial_year_end.year": 2040,
                        "amount.sum": 234,
                    },
                ],
                [
                    {
                        "amount_type.code": "AUDA",
                        "amount_type.label": "Audited",
                        "financial_year_end.year": 2040,
                        "amount.sum": 345,
                    },
                    {
                        "amount_type.code": "ORGB",
                        "amount_type.label": "Budget",
                        "financial_year_end.year": 2041,
                        "amount.sum": 456,
                    },
                ],
            ),
        )
        self.assertEqual(expected, actual)

class AdjustmentsCalculatorTests(SimpleTestCase):
    maxDiff = None

    def test_combine_v1_v2(self):
        """
        - v2 is used for the entire year where it has data
        - everything that doesn't overlap must be included
        """

        class TestAdjustmentsCalculator(AdjustmentsCalculator):
            v1_api_data_key = "v1_key"
            v2_api_data_key = "v2_key"
            v1_group_lookup = {"1000": "A group"}
            v2_group_lookup = {"9000": "A group"}

        api_data = MockAPIData(
            {
                "v1_key": [
                    {
                        "amount_type.code": "AUDA",
                        "financial_year_end.year": 2040,
                        "amount.sum": 3,
                        "item.code": "1000",
                    },
                    {
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2040,
                        "amount.sum": 2,
                        "item.code": "1000",
                    },
                    {
                        "amount_type.code": "AUDA",
                        "financial_year_end.year": 2039,
                        "amount.sum": 30,
                        "item.code": "1000",
                    },
                    {
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2039,
                        "amount.sum": 20,
                        "item.code": "1000",
                    },
                ],
                "v2_key": [
                    {
                        "amount_type.code": "AUDA",
                        "financial_year_end.year": 2040,
                        "amount.sum": 300,
                        "item.code": "9000",
                    },
                    {
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2040,
                        "item.code": "9000",
                        "amount.sum": 200,
                    },
                    {
                        "amount_type.code": "AUDA",
                        "financial_year_end.year": 2041,
                        "amount.sum": 3000,
                        "item.code": "9000",
                    },
                    {
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2041,
                        "item.code": "9000",
                        "amount.sum": 2000,
                    },
                ],
            },
            2040,
        )
        result = TestAdjustmentsCalculator.get_muni_specifics(api_data)
        self.assertEqual(
            {
                2039: [
                    {
                        "amount": None,
                        "comparison": "Original to adjusted budget",
                        "item": "A group",
                        "percent_changed": None,
                    },
                    {
                        "amount": 10,
                        "comparison": "Original budget to audited outcome",
                        "item": "A group",
                        "percent_changed": 50.0,
                    },
                ],
                2040: [
                    {
                        "amount": None,
                        "comparison": "Original to adjusted budget",
                        "item": "A group",
                        "percent_changed": None,
                    },
                    {
                        "amount": 100,
                        "comparison": "Original budget to audited outcome",
                        "item": "A group",
                        "percent_changed": 50.0,
                    },
                ],
                2041: [
                    {
                        "amount": None,
                        "comparison": "Original to adjusted budget",
                        "item": "A group",
                        "percent_changed": None,
                    },
                    {
                        "amount": 1000,
                        "comparison": "Original budget to audited outcome",
                        "item": "A group",
                        "percent_changed": 50.0,
                    },
                ],
            },
            result,
        )

    def test_multiple_years(self):
        class TestAdjustmentsCalculator(AdjustmentsCalculator):
            v1_api_data_key = "v1_key"
            v2_api_data_key = "v2_key"
            v1_group_lookup = dict()
            v2_group_lookup = {"9000": "A group"}

        api_data = MockAPIData(
            {
                "v1_key": [],
                "v2_key": [
                    {
                        "amount_type.code": "AUDA",
                        "financial_year_end.year": 2040,
                        "amount.sum": 300,
                        "item.code": "9000",
                    },
                    {
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2040,
                        "item.code": "9000",
                        "amount.sum": 200,
                    },
                    {
                        "amount_type.code": "AUDA",
                        "financial_year_end.year": 2041,
                        "amount.sum": 3000,
                        "item.code": "9000",
                    },
                    {
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2041,
                        "item.code": "9000",
                        "amount.sum": 2000,
                    },
                ],
            },
            2040,
        )
        result = TestAdjustmentsCalculator.get_muni_specifics(api_data)
        self.assertEqual(
            {
                2040: [
                    {
                        "amount": None,
                        "comparison": "Original to adjusted budget",
                        "item": "A group",
                        "percent_changed": None,
                    },
                    {
                        "amount": 100,
                        "comparison": "Original budget to audited outcome",
                        "item": "A group",
                        "percent_changed": 50.0,
                    },
                ],
                2041:[
                    {
                        "amount": None,
                        "comparison": "Original to adjusted budget",
                        "item": "A group",
                        "percent_changed": None,
                    },
                    {
                        "amount": 1000,
                        "comparison": "Original budget to audited outcome",
                        "item": "A group",
                        "percent_changed": 50.0,
                    },
                ],
            },
            result,
        )

    def test_multiple_items(self):
        class TestAdjustmentsCalculator(AdjustmentsCalculator):
            v1_api_data_key = "v1_key"
            v2_api_data_key = "v2_key"
            v1_group_lookup = dict()
            v2_group_lookup = {"8000": "Another group", "9000": "A group"}

        api_data = MockAPIData(
            {
                "v1_key": [],
                "v2_key": [
                    {
                        "amount_type.code": "AUDA",
                        "financial_year_end.year": 2040,
                        "amount.sum": 300,
                        "item.code": "8000",
                    },
                    {
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2040,
                        "item.code": "8000",
                        "amount.sum": 200,
                    },
                    {
                        "amount_type.code": "AUDA",
                        "financial_year_end.year": 2040,
                        "amount.sum": 3000,
                        "item.code": "9000",
                    },
                    {
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2040,
                        "item.code": "9000",
                        "amount.sum": 2000,
                    },
                ],
            },
            2040,
        )
        result = TestAdjustmentsCalculator.get_muni_specifics(api_data)
        self.assertEqual(
            {
                2040: [
                    {
                        "amount": None,
                        "comparison": "Original to adjusted budget",
                        "item": "A group",
                        "percent_changed": None,
                    },
                    {
                        "amount": 1000,
                        "comparison": "Original budget to audited outcome",
                        "item": "A group",
                        "percent_changed": 50.0,
                    },
                    {
                        "amount": None,
                        "comparison": "Original to adjusted budget",
                        "item": "Another group",
                        "percent_changed": None,
                    },
                    {
                        "amount": 100,
                        "comparison": "Original budget to audited outcome",
                        "item": "Another group",
                        "percent_changed": 50.0,
                    },
                ],
            },
            result,
        )
