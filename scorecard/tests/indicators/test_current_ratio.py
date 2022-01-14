
from ...profile_data import ApiData
from ...profile_data.indicators import (
    CurrentRatio,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    FinancialPositionFactsV2Resource,
    BsheetFactsV1Resource,
)


class TestCurrentRatio(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(GeographyResource, 'current_ratio/scorecard_geography.csv')
        import_data(BsheetFactsV1Resource, 'current_ratio/bsheet_facts_v1.csv')
        import_data(
            FinancialPositionFactsV2Resource,
            'current_ratio/financial_position_facts_v2.csv',
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2019, 2019, 2019, "2019q4")
        api_data.fetch_data([
            "bsheet_auda_years", "financial_position_auda_years_v2",
        ])
        # Provide data to indicator
        result = CurrentRatio.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "ratio",
                "values": [
                    {
                        "date": 2019,
                        "year": 2019,
                        "amount_type": "AUDA",
                        "assets": 17848394183,
                        "liabilities": 7873348202,
                        "result": 2.27,
                        "rating": "good",
                        "cube_version": "v2"
                    },
                    {
                        "date": 2018,
                        "year": 2018,
                        "amount_type": "AUDA",
                        "assets": 14254084899,
                        "liabilities": 8561736837,
                        "result": 1.66,
                        "rating": "good",
                        "cube_version": "v2"
                    },
                    {
                        "date": 2017,
                        "year": 2017,
                        "amount_type": "AUDA",
                        "assets": 11891860172,
                        "liabilities": 8848578284,
                        "result": 1.34,
                        "rating": "ave",
                        "cube_version": "v1"
                    },
                    {
                        "date": 2016,
                        "year": 2016,
                        "amount_type": "AUDA",
                        "assets": 12216493069,
                        "liabilities": 9005549657,
                        "result": 1.36,
                        "rating": "ave",
                        "cube_version": "v1"
                    }
                ],
                "ref": {
                    "title": "Circular 71",
                    "url": "http://mfma.treasury.gov.za/Circulars/Pages/Circular71.aspx"
                },
                "last_year": 2019,
                "formula": {
                    "text": "= Current Assets / Current Liabilities",
                    "actual": [
                        "=", 
                        {
                            "cube": "bsheet",
                            "item_codes": ["2150"],
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
            }
        )
