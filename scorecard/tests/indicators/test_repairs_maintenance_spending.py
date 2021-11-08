from django.test import SimpleTestCase
from ...profile_data import ApiData
from ...profile_data.indicators import (
    RepairsMaintenanceSpending,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    BsheetFactsV1Resource,
    FinancialPositionFactsV2Resource,
    CapitalFactsV1Resource,
    CapitalFactsV2Resource,
)


class MockAPIData:
    years = [2040, 2041, 2042, 2043]
    references = {
        "circular71": {
                "title": "test title",
                "url": "http://example.com",
            },
        }

    def __init__(self, results, budget_year):
        self.results = results
        # self.budget_year = budget_year


class CalculatorTests(SimpleTestCase):
    maxDiff = None

    def test_v1(self):
        """ percentages and ratings are calculated correctly """
        api_data = MockAPIData(
            {
                "repairs_maintenance_v1": [
                    { "financial_year_end.year": 2040, "repairs_maintenance.sum": 1, },
                    { "financial_year_end.year": 2041, "repairs_maintenance.sum": 2, },
                    { "financial_year_end.year": 2042, "repairs_maintenance.sum": 3, },
                    { "financial_year_end.year": 2043, "repairs_maintenance.sum": 4, },
                ],

                "property_plant_equipment_v1": [
                    { "financial_year_end.year": 2040, "property_plant_equipment.sum": 5, },
                    { "financial_year_end.year": 2041, "property_plant_equipment.sum": 6, },
                    { "financial_year_end.year": 2042, "property_plant_equipment.sum": 7, },
                    { "financial_year_end.year": 2043, "property_plant_equipment.sum": 8, },
                ],
                "investment_property_v1": [
                    { "financial_year_end.year": 2040, "investment_property.sum": 9, },
                    { "financial_year_end.year": 2041, "investment_property.sum": 10, },
                    { "financial_year_end.year": 2042, "investment_property.sum": 11, },
                    { "financial_year_end.year": 2043, "investment_property.sum": 12, },
                ],
                "repairs_maintenance_v2": [],
                "property_plant_equipment_v2": [],
                "investment_property_v2": [],
            },
            2040,
        )
        result = RepairsMaintenanceSpending.get_muni_specifics(api_data)
        self.assertEqual(
            [{'date': 2040, 'rating': 'bad', 'result': 7.14},
             {'date': 2041, 'rating': 'good', 'result': 12.5 },
             {'date': 2042, 'rating': 'good', 'result': 16.67 },
             {'date': 2043, 'rating': 'good', 'result': 20.0 }],
            result["values"],
        )

    def test_v2(self):
        """ percentages and ratings are calculated correctly """
        api_data = MockAPIData(
            {
                "repairs_maintenance_v1": [],
                "property_plant_equipment_v1": [],
                "investment_property_v1": [],
                "repairs_maintenance_v2": [
                    { "financial_year_end.year": 2040, "amount.sum": 1, },
                    { "financial_year_end.year": 2041, "amount.sum": 2, },
                    { "financial_year_end.year": 2042, "amount.sum": 3, },
                    { "financial_year_end.year": 2043, "amount.sum": 4, },
                ],
                "property_plant_equipment_v2": [
                    { "financial_year_end.year": 2040, "amount.sum": 5, },
                    { "financial_year_end.year": 2041, "amount.sum": 6, },
                    { "financial_year_end.year": 2042, "amount.sum": 7, },
                    { "financial_year_end.year": 2043, "amount.sum": 8, },
                ],
                "investment_property_v2": [
                    { "financial_year_end.year": 2040, "amount.sum": 9, },
                    { "financial_year_end.year": 2041, "amount.sum": 10, },
                    { "financial_year_end.year": 2042, "amount.sum": 11, },
                    { "financial_year_end.year": 2043, "amount.sum": 12, },
                ],
            },
            2040,
        )
        result = RepairsMaintenanceSpending.get_muni_specifics(api_data)
        self.assertEqual(
            [{'date': 2040, 'rating': 'bad', 'result': 7.14},
             {'date': 2041, 'rating': 'good', 'result': 12.5 },
             {'date': 2042, 'rating': 'good', 'result': 16.67 },
             {'date': 2043, 'rating': 'good', 'result': 20.0 }],
            result["values"],
        )

class TestRepairsMaintenanceSpending(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'repairs_maintenance_spending/scorecard_geography.csv'
        )
        import_data(
            BsheetFactsV1Resource,
            'repairs_maintenance_spending/bsheet_facts_v1.csv'
        )
        import_data(
            FinancialPositionFactsV2Resource,
            'repairs_maintenance_spending/financial_position_facts_v2.csv'
        )
        import_data(
            CapitalFactsV1Resource,
            'repairs_maintenance_spending/capital_facts_v1.csv'
        )
        import_data(
            CapitalFactsV2Resource,
            'repairs_maintenance_spending/capital_facts_v2.csv'
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2019, 2019, 2019, '2019q4')
        api_data.fetch_data([
            "repairs_maintenance_v1",
            "repairs_maintenance_v2",
            "property_plant_equipment_v1",
            "property_plant_equipment_v2",
            "investment_property_v1",
            "investment_property_v2",
        ])
        # Provide data to indicator
        result = RepairsMaintenanceSpending.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "%",
                "values": [
                    {
                        "date": 2019,
                        "result": 0.98,
                        "rating": "bad"
                    },
                    {
                        "date": 2018,
                        "result": 1.08,
                        "rating": "bad"
                    },
                    {
                        "date": 2017,
                        "result": 9.01,
                        "rating": "good"
                    },
                    {
                        "date": 2016,
                        "result": 8.78,
                        "rating": "good"
                    }
                ],
                "ref": {
                    "title": "Circular 71",
                    "url": "http://mfma.treasury.gov.za/Circulars/Pages/Circular71.aspx"
                },
                "last_year": 2019,
                "formula": {
                    "text": "= (Repairs and maintenance expenditure / (Property, Plant and Equipment + Investment Property)) * 100",
                    "actual": [
                        "=", 
                        "(",
                        {
                            "cube": "capital",
                            "item_codes": ["4100"],
                            "amount_type": "AUDA",
                        },
                        "/",
                        "(",
                        {
                            "cube": "bsheet",
                            "item_codes": ["1300"],
                            "amount_type": "AUDA",
                        },
                        "+",
                        {
                            "cube": "bsheet",
                            "item_codes": ["1401"],
                            "amount_type": "AUDA",
                        },
                        ")",
                        ")",
                        "*",
                        "100",
                    ],
                },
            },
        )
