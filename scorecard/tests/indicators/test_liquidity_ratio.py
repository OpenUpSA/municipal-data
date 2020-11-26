
from municipal_finance.resources import (
    BsheetFactsV2Resource,
    BsheetFactsV1Resource,
)

from ...resources import GeographyResource
from ...profile_data import (
    ApiData,
    LiquidityRatio,
)

from . import (
    import_data,
    _IndicatorTestCase,
)


class TestLiquidityRatio(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'liquidity_ratio/scorecard_geography.csv',
        )
        import_data(
            BsheetFactsV1Resource,
            'liquidity_ratio/bsheet_facts_v1.csv',
        )
        import_data(
            BsheetFactsV2Resource,
            'liquidity_ratio/bsheet_facts_v2.csv',
        )
        # Fetch data from API
        api_data = ApiData(self.client, "CPT", 2019, 2019, 2019, "2019q4")
        api_data.fetch_data(["bsheet_auda_years", "bsheet_auda_years_v2"])
        # Provide data to indicator
        result = LiquidityRatio.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "ratio",
                "values": [
                    {
                        "date": "2019",
                        "year": 2019,
                        "amount_type": "ACT",
                        "cash": 310860909,
                        "call_investment_deposits": 10820193529,
                        "liabilities": 7873348202,
                        "result": 1.41,
                        "rating": "good"
                    },
                    {
                        "date": "2018",
                        "year": 2018,
                        "amount_type": "ACT",
                        "cash": 252758618,
                        "call_investment_deposits": 7437051280,
                        "liabilities": 8561736837,
                        "result": 0.9,
                        "rating": "bad"
                    },
                    {
                        "date": "2017",
                        "year": 2017,
                        "amount_type": "ACT",
                        "cash": 591533349,
                        "call_investment_deposits": 4841454888,
                        "liabilities": 8848578284,
                        "result": 0.61,
                        "rating": "bad"
                    },
                    {
                        "date": "2016",
                        "year": 2016,
                        "amount_type": "ACT",
                        "cash": 155633877,
                        "call_investment_deposits": 5803468186,
                        "liabilities": 9005549657,
                        "result": 0.66,
                        "rating": "bad"
                    }
                ],
                "ref": {
                    "title": "Municipal Budget and Reporting Regulations",
                    "url": "http://mfma.treasury.gov.za/RegulationsandGazettes/Municipal%20Budget%20and%20Reporting%20Regulations/Pages/default.aspx"
                }
            }
        )
