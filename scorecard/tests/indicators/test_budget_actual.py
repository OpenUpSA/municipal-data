from django.test import SimpleTestCase
from ...profile_data.indicators.budget_actual import TimeSeriesCalculator, combine_versions


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
            2040
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
            result
        )


    def test_combine_versions(self):
        expected = [
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
        actual = combine_versions(
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
        self.assertEqual(expected, actual)
