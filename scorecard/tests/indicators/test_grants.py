from django.test import TestCase
from ...profile_data.indicators import Grants
from constance.test import override_config


class MockAPIData:
    def __init__(self, results):
        self.results = results


class GrantsTests(TestCase):
    def test_group_years(self):
        """Data is grouped by year. Order of values does not matter."""
        api_data = MockAPIData(
            {
                "grants_v1": [
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "USDG",
                        "grant.label": "Urban Settlement Development Grant",
                    },
                    {
                        "amount.sum": 1109523658.0,
                        "amount_type.code": "ACT",
                        "financial_year_end.year": 2019,
                        "grant.code": "USDG",
                        "grant.label": "Urban Settlement Development Grant",
                    },
                    {
                        "amount.sum": 24266000.0,
                        "amount_type.code": "TRFR",
                        "financial_year_end.year": 2018,
                        "grant.code": "PWPG",
                        "grant.label": "Expanded Public Works Programme Integrated Grant (Municipality)",
                    },
                    {
                        "amount.sum": 5000000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2018,
                        "grant.code": "INEG",
                        "grant.label": "Integrated National Electrification Programme (Municipal) Grant",
                    },
                ],
                "grants_v2": [],
            }
        )
        result = Grants.get_muni_specifics(api_data)
        self.assertEqual(
            {
                2019: [
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "USDG",
                        "grant.label": "Urban Settlement Development Grant",
                    },
                    {
                        "amount.sum": 1109523658.0,
                        "amount_type.code": "ACT",
                        "financial_year_end.year": 2019,
                        "grant.code": "USDG",
                        "grant.label": "Urban Settlement Development Grant",
                    },
                ],
                2018: [
                    {
                        "amount.sum": 24266000.0,
                        "amount_type.code": "TRFR",
                        "financial_year_end.year": 2018,
                        "grant.code": "PWPG",
                        "grant.label": "Expanded Public Works Programme Integrated Grant (Municipality)",
                    },
                    {
                        "amount.sum": 5000000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2018,
                        "grant.code": "INEG",
                        "grant.label": "Integrated National Electrification Programme (Municipal) Grant",
                    },
                ],
            },
            result["national_conditional_grants"],
        )

    def test_exclude_zeros(self):
        """Values that are zero are excluded from results"""
        api_data = MockAPIData(
            {
                "grants_v1": [
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "0001",
                        "grant.label": "Health",
                    },
                    {
                        "amount.sum": 0.0,
                        "amount_type.code": "ACT",
                        "financial_year_end.year": 2019,
                        "grant.code": "0001",
                        "grant.label": "Health",
                    },
                ],
                "grants_v2": [],
            }
        )
        result = Grants.get_muni_specifics(api_data)
        self.assertEqual(
            {
                2019: [
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "0001",
                        "grant.label": "Health",
                    },
                ],
            },
            result["provincial_transfers"],
        )

    @override_config(GRANTS_LATEST_YEAR=2040, GRANTS_LATEST_QUARTER=2)
    def test_data_date(self):
        """The configured date of the recency of the grant data is included"""

        result = Grants.get_muni_specifics(MockAPIData({
            "grants_v1": [],
            "grants_v2": [],
        }))
        self.assertEqual(
            {
                "year": 2040,
                "quarter": 2,
            },
            result["snapshot_date"],
        )

    def test_splitting(self):
        api_data = MockAPIData(
            {
                "grants_v1": [
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "ESG",
                        "grant.label": "Equitable Share Grant",
                    },
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "0012",
                        "grant.label": "Education",
                    },
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "ABC",
                        "grant.label": "ABC grant",
                    },
                ],
                "grants_v2": [],
            }
        )
        result = Grants.get_muni_specifics(api_data)
        self.assertEqual(
            {
                2019: [
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "0012",
                        "grant.label": "Education",
                    },
                ],
            },
            result["provincial_transfers"],
        )
        self.assertEqual(
            {
                2019: [
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "ABC",
                        "grant.label": "ABC grant",
                    },
                ],
            },
            result["national_conditional_grants"],
        )
        self.assertEqual(
            {
                2019: [
                    {
                        "amount.sum": 1484790000.0,
                        "amount_type.code": "ORGB",
                        "financial_year_end.year": 2019,
                        "grant.code": "ESG",
                        "grant.label": "Equitable Share Grant",
                    },
                ],
            },
            result["equitable_share"],
        )

    def test_totals(self):
        result = Grants.totals({
            "national_conditional_grants": {
                2030: [
                    {
                        "amount.sum": 1,
                        "amount_type.code": "A",
                    },
                    {
                        "amount.sum": 2,
                        "amount_type.code": "A",
                    },
                    {
                        "amount.sum": 3,
                        "amount_type.code": "B",
                    },
                ],
                2031: [
                    {
                        "amount.sum": 4,
                        "amount_type.code": "A",
                    },
                    {
                        "amount.sum": 5,
                        "amount_type.code": "A",
                    },
                ],
            },
            "provincial_transfers": {
                2030: [
                    {
                        "amount.sum": 6,
                        "amount_type.code": "A",
                    },
                ],
                2031: [
                    {
                        "amount.sum": 7,
                        "amount_type.code": "B",
                    },
                    {
                        "amount.sum": 8,
                        "amount_type.code": "B",
                    },
                ],
            },
            "equitable_share": {
                2030: [
                    {
                        "amount.sum": 9,
                        "amount_type.code": "A",
                    },
                ],
                2029: [
                    {
                        "amount.sum": 10,
                        "amount_type.code": "C",
                    },
                ],
            },
        })
        expected = {
            2029: {
                "C": {
                    "equitable_share": 10,
                },
            },
            2030: {
                "A": {
                    "national_conditional_grants": 3,
                    "provincial_transfers":  6,
                    "equitable_share": 9,
                },
                "B": {
                    "national_conditional_grants": 3,
                },
            },
            2031: {
                "A": {
                    "national_conditional_grants": 9,
                },
                "B": {
                    "provincial_transfers": 15,
                },
            },
        }
        # assertEqual also compares types so we use assertTrue. pretty is for presentation.
        pretty = {k: dict(v) for k, v in result.items()}
        self.assertTrue(
            expected == result,
            f"\n{expected}\n\n!=\n\n{pretty}"
        )
