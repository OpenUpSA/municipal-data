
from municipal_finance.resources import (
    CapitalFactsV1Resource,
    CapitalFactsV2Resource,
)

from ...resources import GeographyResource
from ...profile_data import (
    ApiData,
    CapitalBudgetSpending,
)

from . import (
    import_data,
    _IndicatorTestCase,
)


class TestCapitalBudgetSpending(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'capital_budget_spending/scorecard_geography.csv'
        )
        import_data(
            CapitalFactsV1Resource,
            'capital_budget_spending/capital_facts_v1.csv'
        )
        import_data(
            CapitalFactsV2Resource,
            'capital_budget_spending/capital_facts_v2.csv'
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2019, 2019, 2019, '2019q4')
        api_data.fetch_data([
            "capital_expenditure_budget_v1",
            "capital_expenditure_actual_v1",
            "capital_expenditure_budget_v2",
            "capital_expenditure_actual_v2",
        ])
        # Provide data to indicator
        result = CapitalBudgetSpending.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "values": [
                    {
                        "date": 2019,
                        "result": 11.73,
                        "overunder": "over",
                        "rating": "ave"
                    },
                    {
                        "date": 2018,
                        "result": -35.51,
                        "overunder": "under",
                        "rating": "bad"
                    },
                    {
                        "date": 2017,
                        "result": -7.37,
                        "overunder": "under",
                        "rating": "ave"
                    },
                    {
                        "date": 2016,
                        "result": -11.46,
                        "overunder": "under",
                        "rating": "ave"
                    }
                ],
                "ref": {
                    "title": "Over and under spending reports to parliament",
                    "url": "http://mfma.treasury.gov.za/Media_Releases/Reports%20to%20Parliament/Pages/default.aspx"
                }
            },
        )
