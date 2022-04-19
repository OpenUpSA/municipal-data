
from ...profile_data import ApiData
from ...profile_data.indicators import (
    UIFWExpenditure,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    IncexpFactsV2Resource,
    IncexpFactsV1Resource,
    UIFWExpenseFactsResource,
)


class TestUIFWExpenditure(_IndicatorTestCase):

    def setUp(self):
        super().setUp()
        # Load sample data
        import_data(
            GeographyResource,
            'uifw_expenditure/scorecard_geography.csv',
        )
        import_data(
            UIFWExpenseFactsResource,
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
        
    def test_same_as_last_audit_year(self):
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2020, 2019, 2020, '2019q4')
        api_data.fetch_data([
            "uifw_expenditure",
            "operating_expenditure_actual_v1",
            "operating_expenditure_actual_v2",
        ])
        # Provide data to indicator
        result = UIFWExpenditure.get_muni_specifics(api_data)
        self.assertEqual(
            {
                "result_type": "%",
                "values": [
                    {
                        "date": 2020,
                        "result": 0.06,
                        "rating": "bad",
                        "cube_version": "v2"
                    },
                    {
                        "date": 2019,
                        "result": 2.66,
                        "rating": "bad",
                        "cube_version": "v1"
                    },
                    {
                        "date": 2018,
                        "result": 0.69,
                        "rating": "bad",
                        "cube_version": "v1"
                    },
                    {
                        "date": 2017,
                        "result": 0.14,
                        "rating": "bad",
                        "cube_version": "v1"
                    },
                ],
                "ref": {
                    "title": "Circular 71",
                    "url": "http://mfma.treasury.gov.za/Circulars/Pages/Circular71.aspx"
                },
                "last_year": 2020,
                "formula": {
                    "text": "= (Unauthorised, Irregular, Fruitless and Wasteful Expenditure / Actual Operating Expenditure) * 100",
                    "actual": [
                        "=",
                        "(",
                        {
                            "cube": "uifwexp",
                            "item_codes": ["irregular", "fruitless", "unauthorised"],
                        },
                        "/",
                        {
                            "cube": "incexp",
                            "item_codes": ["4600"],
                            "amount_type": "AUDA",
                        },
                        ")",
                        "*",
                        "100",
                    ],
                },
                "formula_v2": {
                    "text": "= (Unauthorised, Irregular, Fruitless and Wasteful Expenditure / Actual Operating Expenditure) * 100",
                    "actual": [
                        "=",
                        "(",
                        {
                            "cube": "uifwexp",
                            "item_codes": ["irregular", "fruitless", "unauthorised"],
                        },
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
                            "amount_type": "AUDA",
                        },
                        ")",
                        "*",
                        "100",
                    ],
                },
            },
            result,
        )

    def test_uifw_lagging_one_year(self):
        """
        Demonstrate that if last uifw year lags one year behind last audit
        year, we still only calculate 4 years up to the last UIFW year.
        """
        api_data = ApiData(self.api_client, "CPT", 2021, 2019, 2020, '2019q4')
        api_data.fetch_data([
            "uifw_expenditure",
            "operating_expenditure_actual_v1",
            "operating_expenditure_actual_v2",
        ])
        # Provide data to indicator
        result = UIFWExpenditure.get_muni_specifics(api_data)
        self.assertEqual(
            [
                {
                    "date": 2020,
                    "result": 0.06,
                    "rating": "bad",
                    "cube_version": "v2"
                },
                {
                    "date": 2019,
                    "result": 2.66,
                    "rating": "bad",
                    "cube_version": "v1"
                },
                {
                    "date": 2018,
                    "result": 0.69,
                    "rating": "bad",
                    "cube_version": "v1"
                },
                {
                    "date": 2017,
                    "result": 0.14,
                    "rating": "bad",
                    "cube_version": "v1"
                },
            ],
            result["values"],
        )
        self.assertEqual(
            2020
            result["last_year"],
        )
        
