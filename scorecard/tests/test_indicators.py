import tablib

from django.test import TestCase, override_settings

from municipal_finance.resources import (
    BsheetFactsV2Resource,
    BsheetFactsV1Resource,
)

from ..profile_data import (
    ApiClient,
    ApiData,
    CurrentRatio,
    LiquidityRatio,
)


@override_settings(
    SITE_ID=3,
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
)
class TestIndicators(TestCase):

    def setUp(self):
        # Load sample data
        BsheetFactsV1Resource().import_data(
            tablib.Dataset().load(
                open('scorecard/fixtures/tests/indicators/bsheet_facts_v1.csv')
            ),
            raise_errors=True,
        )
        BsheetFactsV2Resource().import_data(
            tablib.Dataset().load(
                open('scorecard/fixtures/tests/indicators/bsheet_facts_v2.csv')
            ),
            raise_errors=True,
        )

    def test_current_ratio(self):
        # Setup the API client
        client = ApiClient(lambda u, p: self.client.get(u, data=p), "/api")
        # Fetch data from API
        api_data = ApiData(lambda q: client.api_get(q), "CPT")
        api_data.fetch_data(["in_year_bsheet", "in_year_bsheet_v2"])
        # Provide data to indicator
        result = CurrentRatio.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "values": [
                    {
                        "date": "2020q4",
                        "year": 2020,
                        "quarter": 4,
                        "month": 12,
                        "amount_type": "ACT",
                        "assets": 232776021,
                        "liabilities": 2671817149,
                        "result": 0.09,
                        "rating": "bad"
                    },
                    {
                        "date": "2020q3",
                        "year": 2020,
                        "quarter": 3,
                        "month": 9,
                        "amount_type": "ACT",
                        "assets": 107720360773,
                        "liabilities": 108799426256,
                        "result": 0.99,
                        "rating": "bad"
                    },
                    {
                        "date": "2020q2",
                        "year": 2020,
                        "quarter": 2,
                        "month": 6,
                        "amount_type": "ACT",
                        "assets": -313837726,
                        "liabilities": 194186052,
                        "result": -1.62,
                        "rating": "bad"
                    },
                    {
                        "date": "2020q1",
                        "year": 2020,
                        "quarter": 1,
                        "month": 3,
                        "amount_type": "ACT",
                        "assets": -170890337,
                        "liabilities": 46786182,
                        "result": -3.65,
                        "rating": "bad"
                    },
                    {
                        "date": "2019q4",
                        "year": 2019,
                        "quarter": 4,
                        "month": 12,
                        "amount_type": "ACT",
                        "assets": 14449883217,
                        "liabilities": 8297566444,
                        "result": 1.74,
                        "rating": "good"
                    }
                ],
                "ref": {
                    "title": "Circular 71",
                    "url": "http://mfma.treasury.gov.za/Circulars/Pages/Circular71.aspx"
                }
            }
        )

    def test_liquidity_ratio(self):
        # Setup the API client
        client = ApiClient(lambda u, p: self.client.get(u, data=p), "/api")
        # Fetch data from API
        api_data = ApiData(lambda q: client.api_get(q), "CPT")
        api_data.fetch_data(["in_year_bsheet", "in_year_bsheet_v2"])
        # Provide data to indicator
        result = LiquidityRatio.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "values": [
                    {
                        "date": "2020q4",
                        "year": 2020,
                        "quarter": 4,
                        "month": 12,
                        "amount_type": "ACT",
                        "cash": -11623447,
                        "call_investment_deposits": -23865811,
                        "liabilities": 2671817149,
                        "result": -0.01,
                        "rating": "bad"
                    },
                    {
                        "date": "2020q3",
                        "year": 2020,
                        "quarter": 3,
                        "month": 9,
                        "amount_type": "ACT",
                        "cash": -127956183,
                        "call_investment_deposits": -8091248,
                        "liabilities": 108799426256,
                        "result": 0,
                        "rating": "bad"
                    },
                    {
                        "date": "2020q2",
                        "year": 2020,
                        "quarter": 2,
                        "month": 6,
                        "amount_type": "ACT",
                        "cash": -133467086,
                        "call_investment_deposits": 6620209,
                        "liabilities": 194186052,
                        "result": -0.65,
                        "rating": "bad"
                    },
                    {
                        "date": "2020q1",
                        "year": 2020,
                        "quarter": 1,
                        "month": 3,
                        "amount_type": "ACT",
                        "cash": -80061135,
                        "call_investment_deposits": 3014575,
                        "liabilities": 46786182,
                        "result": -1.65,
                        "rating": "bad"
                    },
                    {
                        "date": "2019q4",
                        "year": 2019,
                        "quarter": 4,
                        "month": 12,
                        "amount_type": "ACT",
                        "cash": 304135337,
                        "call_investment_deposits": 7389433226,
                        "liabilities": 8297566444,
                        "result": 0.93,
                        "rating": "bad"
                    }
                ],
                "ref": {
                    "title": "Municipal Budget and Reporting Regulations",
                    "url": "http://mfma.treasury.gov.za/RegulationsandGazettes/Municipal%20Budget%20and%20Reporting%20Regulations/Pages/default.aspx"
                }
            }
        )
