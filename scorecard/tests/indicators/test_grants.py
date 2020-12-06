from django.test import TestCase
from ...profile_data.indicators import Grants


class MockAPIData:
    def __init__(self, results):
        self.results = results


class GrantsTests(TestCase):
    def test_group_years(self):
        """Data is grouped by year. Order of values does not matter."""
        api_data = MockAPIData({
            "grants_v1": [
                {'amount.sum': 1484790000.0,
                 'amount_type.code': 'ORGB',
                 'financial_year_end.year': 2019,
                 'grant.code': 'USDG',
                 'grant.label': 'Urban Settlement Development Grant'},
                {'amount.sum': 1109523658.0,
                 'amount_type.code': 'ACT',
                 'financial_year_end.year': 2019,
                 'grant.code': 'USDG',
                 'grant.label': 'Urban Settlement Development Grant'},
                {'amount.sum': 24266000.0,
                 'amount_type.code': 'TRFR',
                 'financial_year_end.year': 2018,
                 'grant.code': 'PWPG',
                 'grant.label': 'Expanded Public Works Programme Integrated Grant (Municipality)'},
                {'amount.sum': 5000000.0,
                 'amount_type.code': 'ORGB',
                 'financial_year_end.year': 2018,
                 'grant.code': 'INEG',
                 'grant.label': 'Integrated National Electrification Programme (Municipal) Grant'},
            ]
        })
        result = Grants.get_muni_specifics(api_data)
        self.assertEqual(
            {
                2019: [
                    {'amount.sum': 1484790000.0,
                     'amount_type.code': 'ORGB',
                     'financial_year_end.year': 2019,
                     'grant.code': 'USDG',
                     'grant.label': 'Urban Settlement Development Grant'},
                    {'amount.sum': 1109523658.0,
                     'amount_type.code': 'ACT',
                     'financial_year_end.year': 2019,
                     'grant.code': 'USDG',
                     'grant.label': 'Urban Settlement Development Grant'},
                ],
                2018: [
                    {'amount.sum': 24266000.0,
                     'amount_type.code': 'TRFR',
                     'financial_year_end.year': 2018,
                     'grant.code': 'PWPG',
                     'grant.label': 'Expanded Public Works Programme Integrated Grant (Municipality)'},
                    {'amount.sum': 5000000.0,
                     'amount_type.code': 'ORGB',
                     'financial_year_end.year': 2018,
                     'grant.code': 'INEG',
                     'grant.label': 'Integrated National Electrification Programme (Municipal) Grant'},
                ]
            },
            result["values"]
        )

    def test_exclude_zeros(self):
        """Values that are zero are excluded from results"""
        self.assertFalse(True)

    def test_year_combines_amount_types(self):
        """
        All amount types included in the same year result list, to be grouped
        by the chart.
        """
        self.assertFalse(True)

    def test_data_date(self):
        """The configured date of the recency of the grant data is included"""
        self.assertFalse(True)
