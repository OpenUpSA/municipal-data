from ...profile_data import ApiData
from ...profile_data.indicators import (
    CurrentDebtorsCollectionRate,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    CashFlowFactsV1Resource,
    CashFlowFactsV2Resource,
    IncexpFactsV1Resource,
    IncexpFactsV2Resource,
)


class TestCurrentDebtorsCollectionRate(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'current_debtors_collection_rate/scorecard_geography.csv'
        )
        import_data(
            CashFlowFactsV1Resource,
            'current_debtors_collection_rate/cflow_facts_v1.csv'
        )
        import_data(
            CashFlowFactsV2Resource,
            'current_debtors_collection_rate/cflow_facts_v2.csv'
        )
        import_data(
            IncexpFactsV1Resource,
            'current_debtors_collection_rate/incexp_facts_v1.csv'
        )
        import_data(
            IncexpFactsV2Resource,
            'current_debtors_collection_rate/incexp_facts_v2.csv'
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2020, 2020, 2020, "2019q4")
        api_data.fetch_data([
            "cflow_auda_years", "cflow_auda_years_v2",
            "incexp_auda_years", "incexp_auda_years_v2",
        ])
        # Provide data to indicator
        result = CurrentDebtorsCollectionRate.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "%",
                "values": [
                    {
                        "year": 2020,
                        "date": "2020",
                        "amount_type": "AUDA",
                        "result": -0.58,
                        "rating": "bad",
                        "cube_version": "v2"
                    },
                    {
                        "year": 2019,
                        "date": "2019",
                        "amount_type": "AUDA",
                        "result": -0.15,
                        "rating": "bad",
                        "cube_version": "v1"
                    },
                    {
                        "year": 2018,
                        "date": "2018",
                        "amount_type": "AUDA",
                        "result": 131.34,
                        "rating": "good",
                        "cube_version": "v1"
                    },
                    {
                        "year": 2017,
                        "date": "2017",
                        "amount_type": "AUDA",
                        "result": 96.76,
                        "rating": "good",
                        "cube_version": "v1"
                    }
                ],
                "ref": {
                    "title": "Municipal Budget and Reporting Regulations",
                    "url": "http://mfma.treasury.gov.za/RegulationsandGazettes/Municipal%20Budget%20and%20Reporting%20Regulations/Pages/default.aspx"
                },
                "last_year": 2020,
                "formula": {
                    "text": "= (Collected Revenue / Billed Revenue) * 100",
                    "actual": [
                        "=", 
                        "(",
                        {
                            "cube": "cflow",
                            "item_codes": [
                                "3010", "3030", "3040", "3050", "3060", "3070", "3100",
                            ],
                            "amount_type": "AUDA",
                        },
                        "/",
                        {
                            "cube": "incexp",
                            "item_codes": [
                                "0200", "0400", "1000",
                            ],
                            "amount_type": "AUDA",
                        },
                        ")",
                        "*",
                        "100",
                    ],
                },
                "formula_v2": {
                    "text": "= (Collected Revenue / Billed Revenue) * 100",
                    "actual": [
                        "=", 
                        "(",
                        {
                            "cube": "cflow_v2",
                            "item_codes": [
                                "0120", "0130", "0280",
                            ],
                            "amount_type": "AUDA",
                        },
                        "/",
                        {
                            "cube": "incexp_v2",
                            "item_codes": [
                                "0200", "0300", "0400", "0500", "0600", "0800", "0900", "1000",
                            ],
                            "amount_type": "AUDA",
                        },
                        ")",
                        "*",
                        "100",
                    ],
                },
            }
        )
