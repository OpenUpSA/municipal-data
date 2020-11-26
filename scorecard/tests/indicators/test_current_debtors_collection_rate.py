
from municipal_finance.resources import (
    CashflowFactsV1Resource,
    CashflowFactsV2Resource,
    IncexpFactsV1Resource,
    IncexpFactsV2Resource,
)

from ...resources import GeographyResource
from ...profile_data import (
    ApiData,
    CurrentDebtorsCollectionRate,
)

from . import (
    import_data,
    _IndicatorTestCase,
)


class TestCurrentDebtorsCollectionRate(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'current_debtors_collection_rate/scorecard_geography.csv'
        )
        import_data(
            CashflowFactsV1Resource,
            'current_debtors_collection_rate/cflow_facts_v1.csv'
        )
        import_data(
            CashflowFactsV2Resource,
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
        api_data = ApiData(self.client, "CPT", 2019, 2019, 2019, "2019q4")
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
                        "year": 2019,
                        "date": "2019",
                        "amount_type": "AUDA",
                        "result": -0.58,
                        "rating": "bad"
                    },
                    {
                        "year": 2018,
                        "date": "2018",
                        "amount_type": "AUDA",
                        "result": -0.15,
                        "rating": "bad"
                    },
                    {
                        "year": 2017,
                        "date": "2017",
                        "amount_type": "AUDA",
                        "result": 96.76,
                        "rating": "good"
                    },
                    {
                        "year": 2016,
                        "date": "2016",
                        "amount_type": "AUDA",
                        "result": 99.39,
                        "rating": "good"
                    }
                ],
                "ref": {
                    "title": "Municipal Budget and Reporting Regulations",
                    "url": "http://mfma.treasury.gov.za/RegulationsandGazettes/Municipal%20Budget%20and%20Reporting%20Regulations/Pages/default.aspx"
                }
            }
        )
