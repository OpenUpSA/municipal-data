from ...profile_data import ApiData
from ...profile_data.indicators import (
    CashBalance,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    CashFlowFactsV1Resource,
    CashFlowFactsV2Resource,
)


class TestCashBalance(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'cash_balance/scorecard_geography.csv'
        )
        import_data(
            CashFlowFactsV1Resource,
            'cash_balance/cash_flow_facts_v1.csv'
        )
        import_data(
            CashFlowFactsV2Resource,
            'cash_balance/cash_flow_facts_v2.csv'
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2020, 2020, 2020, '2020q4')
        api_data.fetch_data([
            "cash_flow_v1",
            "cash_flow_v2",
        ])
        # Provide data to indicator
        result = CashBalance.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "R",
                "values": [
                    {
                        "date": 2020,
                        "result": 7101183182.0,
                        "rating": "good",
                        "cube_version": "v2"
                    },
                    {
                        "date": 2019,
                        "result": -3448597019.0,
                        "rating": "bad",
                        "cube_version": "v1"
                    },
                    {
                        "date": 2018,
                        "result": 5806824000.0,
                        "rating": "good",
                        "cube_version": "v1"
                    },
                    {
                        "date": 2017,
                        "result": 3773576000.0,
                        "rating": "good",
                        "cube_version": "v1"
                    }
                ],
                "ref": {
                    "title": "State of Local Government Finances",
                    "url": "http://mfma.treasury.gov.za/Media_Releases/The%20state%20of%20local%20government%20finances/Pages/default.aspx"
                },
                "last_year": 2020,
                "formula": {
                    "text": "= Cash available at year end",
                    "actual": [
                        "=", 
                        {
                            "cube": "cflow",
                            "item_codes": ["4200"],
                            "amount_type": "AUDA",
                        }
                    ],
                },
                "formula_v2": {
                    "text": "= Cash available at year end",
                    "actual": [
                        "=", 
                        {
                            "cube": "cflow_v2",
                            "item_codes": ["0430"],
                            "amount_type": "AUDA",
                        }
                    ],
                },
            }
        )
