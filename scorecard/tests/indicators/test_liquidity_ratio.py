
from ...profile_data import ApiData
from ...profile_data.indicators import (
    LiquidityRatio,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    BsheetFactsV1Resource,
    FinancialPositionFactsV2Resource,
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
            FinancialPositionFactsV2Resource,
            'liquidity_ratio/financial_position_facts_v2.csv',
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2020, 2020, 2020, "2020q4")
        api_data.fetch_data([
            "bsheet_auda_years", "financial_position_auda_years_v2"
        ])
        # Provide data to indicator
        result = LiquidityRatio.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "ratio",
                "values": [
                    {
                        "date": "2020",
                        "year": 2020,
                        "amount_type": "ACT",
                        "cash": 310860909.0,
                        "call_investment_deposits": 10820193529.0,
                        "liabilities": 7873348202.0,
                        "result": 1.41,
                        "rating": "good",
                        "cube_version": "v2"
                    },
                    {
                        "date": "2019",
                        "year": 2019,
                        "amount_type": "ACT",
                        "cash": 252758618.0,
                        "call_investment_deposits": 7437051280.0,
                        "liabilities": 8561736837.0,
                        "result": 0.9,
                        "rating": "bad",
                        "cube_version": "v1"
                    },
                    {
                        "date": "2018",
                        "year": 2018,
                        "amount_type": "ACT",
                        "cash": 351348850.0,
                        "call_investment_deposits": 7437051180.0,
                        "liabilities": 8994077535.0,
                        "result": 0.87,
                        "rating": "bad",
                        "cube_version": "v1"
                    },
                    {
                        "date": "2017",
                        "year": 2017,
                        "amount_type": "ACT",
                        "cash": 591533349,
                        "call_investment_deposits": 4841454888,
                        "liabilities": 8848578284.0,
                        "result": 0.61,
                        "rating": "bad",
                        "cube_version": "v1"
                    }
                ],
                "ref": {
                    "title": "Municipal Budget and Reporting Regulations",
                    "url": "http://mfma.treasury.gov.za/RegulationsandGazettes/Municipal%20Budget%20and%20Reporting%20Regulations/Pages/default.aspx"
                },
                "last_year": 2020,
                "formula": {
                    "text": "= (Cash + Call Investment Deposits) / Current Liabilities",
                    "actual": [
                        "=", 
                        {
                            "cube": "bsheet",
                            "item_codes": ["1800", "2200"],
                            "amount_type": "AUDA",
                        },
                        "/",
                        {
                            "cube": "bsheet",
                            "item_codes": ["1600"],
                            "amount_type": "AUDA",
                        },
                    ],
                },
                "formula_v2": {
                    "text": "= (Cash + Call Investment Deposits) / Current Liabilities",
                    "actual": [
                        "=", 
                        {
                            "cube": "financial_position_v2",
                            "item_codes": ["0120", "0130"],
                            "amount_type": "AUDA",
                        },
                        "/",
                        {
                            "cube": "financial_position_v2",
                            "item_codes": ["0330", "0340", "0350", "0360", "0370"],
                            "amount_type": "AUDA",
                        },
                    ],
                },
            }
        )
