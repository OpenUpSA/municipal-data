
from municipal_finance.resources import (
    IncexpFactsV1Resource,
    IncexpFactsV2Resource,
)

from ...resources import GeographyResource
from ...profile_data import (
    ApiData,
    OperatingBudgetSpending,
)

from . import (
    import_data,
    _IndicatorTestCase,
)


class TestOperatingBudgetSpending(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'operating_budget_spending/scorecard_geography.csv'
        )
        import_data(
            IncexpFactsV1Resource,
            'operating_budget_spending/income_expenditure_facts_v1.csv'
        )
        import_data(
            IncexpFactsV2Resource,
            'operating_budget_spending/income_expenditure_facts_v2.csv'
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2019, 2019, 2019, '2019q4')
        api_data.fetch_data([
            "operating_expenditure_actual_v1",
            "operating_expenditure_budget_v1",
            "operating_expenditure_actual_v2",
            "operating_expenditure_budget_v2",
        ])
        # Provide data to indicator
        result = OperatingBudgetSpending.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "%",
                "values": [
                    {
                        "date": 2019,
                        "result": -6.8,
                        "rating": "ave",
                        "overunder": "under"
                    },
                    {
                        "date": 2018,
                        "result": -10.6,
                        "rating": "ave",
                        "overunder": "under"
                    },
                    {
                        "date": 2017,
                        "result": -7.6,
                        "rating": "ave",
                        "overunder": "under"
                    },
                    {
                        "date": 2016,
                        "result": -5.2,
                        "rating": "ave",
                        "overunder": "under"
                    }
                ],
                "ref": {
                    "title": "Over and under spending reports to parliament",
                    "url": "http://mfma.treasury.gov.za/Media_Releases/Reports%20to%20Parliament/Pages/default.aspx"
                }
            },
        )
