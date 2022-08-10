
from ...profile_data import ApiData
from ...profile_data.indicators import (
    OperatingBudgetSpending,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    IncexpFactsV1Resource,
    IncexpFactsV2Resource,
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
        api_data = ApiData(self.api_client, "CPT", 2020, 2020, 2020, '2020q4')
        api_data.fetch_data([
            "operating_expenditure_actual_v1",
            "operating_expenditure_budget_v1",
            "operating_expenditure_actual_v2",
            "operating_expenditure_budget_v2",
        ])
        # Provide data to indicator
        result = OperatingBudgetSpending.get_muni_specifics(api_data)
        self.assertEqual(
            {
                "result_type": "%",
                "values": [
                    {
                        "date": 2020,
                        "result": 5.7,
                        "rating": "ave",
                        "overunder": "over",
                        "cube_version": "v2"
                    },
                    {
                        "date": 2019,
                        "result": -6.0,
                        "rating": "ave",
                        "overunder": "under",
                        "cube_version": "v1"
                    },
                    {
                        "date": 2018,
                        "result": -8.1,
                        "rating": "ave",
                        "overunder": "under",
                        "cube_version": "v1"
                    },
                    {
                        "date": 2017,
                        "result": -7.6,
                        "rating": "ave",
                        "overunder": "under",
                        "cube_version": "v1"
                    }
                ],
                "ref": {
                    "title": "Over and under spending reports to parliament",
                    "url": "http://mfma.treasury.gov.za/Media_Releases/Reports%20to%20Parliament/Pages/default.aspx"
                },
                "last_year": 2020,
                "formula": {
                    "text": "= ((Actual Operating Expenditure - Budget Operating Expenditure) / Budgeted Operating Expenditure) * 100",
                    "actual": [
                        "=",
                        "(",
                        "(",
                        {
                            "cube": "incexp",
                            "item_codes": ["4600"],
                            "amount_type": "AUDA",
                        },
                        "-",
                        {
                            "cube": "incexp",
                            "item_codes": ["4600"],
                            "amount_type": "ADJB",
                        },
                        ")",
                        "/",
                        {
                            "cube": "incexp",
                            "item_codes": ["4600"],
                            "amount_type": "ADJB",
                        },
                        ")",
                        "*",
                        "100",
                    ],
                },
                "formula_v2": {
                    "text": "= ((Actual Operating Expenditure - Budget Operating Expenditure) / Budgeted Operating Expenditure) * 100",
                    "actual": [
                        "=",
                        "(",
                        "(",
                        {
                            "cube": "incexp_v2",
                            "item_codes": [
                                '2000',
                                '2100',
                                '2200',
                                '2300',
                                '2400',
                                '2500',
                                '2600',
                                '2700',
                                '2800',
                                '2900',
                                '3000'
                            ],
                            "amount_type": "AUDA",
                        },
                        "-",
                        {
                            "cube": "incexp_v2",
                            "item_codes": [
                                '2000',
                                '2100',
                                '2200',
                                '2300',
                                '2400',
                                '2500',
                                '2600',
                                '2700',
                                '2800',
                                '2900',
                                '3000'
                            ],
                            "amount_type": "ADJB",
                        },
                        ")",
                        "/",
                        {
                            "cube": "incexp_v2",
                            "item_codes": [
                                '2000',
                                '2100',
                                '2200',
                                '2300',
                                '2400',
                                '2500',
                                '2600',
                                '2700',
                                '2800',
                                '2900',
                                '3000'
                            ],
                            "amount_type": "ADJB",
                        },
                        ")",
                        "*",
                        "100",
                    ],
                },
            },
            result,
        )
