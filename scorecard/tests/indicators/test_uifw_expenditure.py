
from municipal_finance.resources import (
    IncexpFactsV2Resource,
    IncexpFactsV1Resource,
    UIFWExpenditureFactsResource,
)

from ...resources import GeographyResource
from ...profile_data import (
    ApiData,
    UIFWExpenditure,
)

from .utils import (
    import_data,
    IndicatorTestCase,
)


class TestUIFWExpenditure(IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'uifw_expenditure/scorecard_geography.csv',
        )
        import_data(
            UIFWExpenditureFactsResource,
            'uifw_expenditure/uifw_expenditure_facts.csv',
        )
        import_data(
            IncexpFactsV1Resource,
            'uifw_expenditure/income_expenditure_facts_v1.csv',
        )
        import_data(
            IncexpFactsV2Resource,
            'uifw_expenditure/income_expenditure_facts_v2.csv',
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT")
        api_data.fetch_data([
            "uifw_expenditure",
            "operating_expenditure_actual_v1",
            "operating_expenditure_actual_v2",
        ])
        # Provide data to indicator
        result = UIFWExpenditure.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "values": [
                    {
                        "date": 2019,
                        "result": 2.68,
                        "rating": "bad"
                    },
                    {
                        "date": 2018,
                        "result": 0.71,
                        "rating": "bad"
                    },
                    {
                        "date": 2017,
                        "result": 0.14,
                        "rating": "bad"
                    },
                    {
                        "date": 2016,
                        "result": 0,
                        "rating": "good"
                    }
                ],
                "ref": {
                    "title": "Circular 71",
                    "url": "http://mfma.treasury.gov.za/Circulars/Pages/Circular71.aspx"
                }
            },
        )
