from ...profile_data import ApiData
from ...profile_data.indicators import (
    ExpenditureFunctionalBreakdown,
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


# expenditure_functional_breakdown
class TestExpenditureFunctionalBreakdown(_IndicatorTestCase):
    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource, "operating_budget_spending/scorecard_geography.csv"
        )
        import_data(
            IncexpFactsV1Resource,
            "operating_budget_spending/income_expenditure_facts_v1.csv",
        )
        import_data(
            IncexpFactsV2Resource,
            "operating_budget_spending/income_expenditure_facts_v2.csv",
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2020, 2020, 2020, "2020q4")
        api_data.fetch_data(
            [
                "expenditure_functional_breakdown",
                "expenditure_functional_breakdown_v2",
            ]
        )
        # Provide data to indicator
        result = ExpenditureFunctionalBreakdown.get_muni_specifics(api_data)

        self.assertEqual(
            {
                "values": [
                    {
                        "amount": 642335159.0,
                        "percent": 1.95,
                        "item": "Community & Social Services",
                        "date": "2017",
                    },
                    {
                        "amount": 9764952152.0,
                        "percent": 29.57,
                        "item": "Electricity ",
                        "date": "2017",
                    },
                    {
                        "amount": 113416863.0,
                        "percent": 0.34,
                        "item": "Environmental Protection",
                        "date": "2017",
                    },
                    {
                        "amount": 6205745326.0,
                        "percent": 18.79,
                        "item": "Governance, Administration, Planning and Development",
                        "date": "2017",
                    },
                    {
                        "amount": 999459766.0,
                        "percent": 3.03,
                        "item": "Health",
                        "date": "2017",
                    },
                    {
                        "amount": 1343676621.0,
                        "percent": 4.07,
                        "item": "Housing",
                        "date": "2017",
                    },
                    {
                        "amount": 242541316.0,
                        "percent": 0.73,
                        "item": "Other",
                        "date": "2017",
                    },
                    {
                        "amount": 2697688277.0,
                        "percent": 8.17,
                        "item": "Public Safety",
                        "date": "2017",
                    },
                    {
                        "amount": 2962138419.0,
                        "percent": 8.97,
                        "item": "Road Transport",
                        "date": "2017",
                    },
                    {
                        "amount": 1350117891.0,
                        "percent": 4.09,
                        "item": "Sport And Recreation",
                        "date": "2017",
                    },
                    {
                        "amount": 1968026884.0,
                        "percent": 5.96,
                        "item": "Waste Management",
                        "date": "2017",
                    },
                    {
                        "amount": 1436777514.0,
                        "percent": 4.35,
                        "item": "Waste Water Management",
                        "date": "2017",
                    },
                    {
                        "amount": 3296754955.0,
                        "percent": 9.98,
                        "item": "Water",
                        "date": "2017",
                    },
                    {
                        "amount": 837312699.0,
                        "percent": 2.44,
                        "item": "Community & Social Services",
                        "date": "2018",
                    },
                    {
                        "amount": 9385677420.0,
                        "percent": 27.35,
                        "item": "Electricity ",
                        "date": "2018",
                    },
                    {
                        "amount": 125801713.0,
                        "percent": 0.37,
                        "item": "Environmental Protection",
                        "date": "2018",
                    },
                    {
                        "amount": 7598669618.0,
                        "percent": 22.14,
                        "item": "Governance, Administration, Planning and Development",
                        "date": "2018",
                    },
                    {
                        "amount": 1068081082.0,
                        "percent": 3.11,
                        "item": "Health",
                        "date": "2018",
                    },
                    {
                        "amount": 1181977044.0,
                        "percent": 3.44,
                        "item": "Housing",
                        "date": "2018",
                    },
                    {
                        "amount": 744322793.0,
                        "percent": 2.17,
                        "item": "Other",
                        "date": "2018",
                    },
                    {
                        "amount": 656863605.0,
                        "percent": 1.91,
                        "item": "Public Safety",
                        "date": "2018",
                    },
                    {
                        "amount": 5284650476.0,
                        "percent": 15.4,
                        "item": "Road Transport",
                        "date": "2018",
                    },
                    {
                        "amount": 1114225213.0,
                        "percent": 3.25,
                        "item": "Sport And Recreation",
                        "date": "2018",
                    },
                    {
                        "amount": 2111879736.0,
                        "percent": 6.15,
                        "item": "Waste Management",
                        "date": "2018",
                    },
                    {
                        "amount": 1181386852.0,
                        "percent": 3.44,
                        "item": "Waste Water Management",
                        "date": "2018",
                    },
                    {
                        "amount": 3026137787.0,
                        "percent": 8.82,
                        "item": "Water",
                        "date": "2018",
                    },
                    {
                        "amount": 883385270.0,
                        "percent": 2.42,
                        "item": "Community & Social Services",
                        "date": "2019",
                    },
                    {
                        "amount": 9934887545.0,
                        "percent": 27.22,
                        "item": "Electricity ",
                        "date": "2019",
                    },
                    {
                        "amount": 144546505.0,
                        "percent": 0.4,
                        "item": "Environmental Protection",
                        "date": "2019",
                    },
                    {
                        "amount": 8950230060.0,
                        "percent": 24.52,
                        "item": "Governance, Administration, Planning and Development",
                        "date": "2019",
                    },
                    {
                        "amount": 1156258229.0,
                        "percent": 3.17,
                        "item": "Health",
                        "date": "2019",
                    },
                    {
                        "amount": 1236545059.0,
                        "percent": 3.39,
                        "item": "Housing",
                        "date": "2019",
                    },
                    {
                        "amount": 318842626.0,
                        "percent": 0.87,
                        "item": "Other",
                        "date": "2019",
                    },
                    {
                        "amount": 643571112.0,
                        "percent": 1.76,
                        "item": "Public Safety",
                        "date": "2019",
                    },
                    {
                        "amount": 5701801276.0,
                        "percent": 15.62,
                        "item": "Road Transport",
                        "date": "2019",
                    },
                    {
                        "amount": 1187603633.0,
                        "percent": 3.25,
                        "item": "Sport And Recreation",
                        "date": "2019",
                    },
                    {
                        "amount": 2300992268.0,
                        "percent": 6.3,
                        "item": "Waste Management",
                        "date": "2019",
                    },
                    {
                        "amount": 1252179065.0,
                        "percent": 3.43,
                        "item": "Waste Water Management",
                        "date": "2019",
                    },
                    {
                        "amount": 2785243355.0,
                        "percent": 7.63,
                        "item": "Water",
                        "date": "2019",
                    },
                    {
                        "amount": 7288097448.0,
                        "percent": 20.15,
                        "item": "Community and public safety",
                        "date": "2020",
                    },
                    {
                        "amount": 4439158290.0,
                        "percent": 12.27,
                        "item": "Economic and environmental services",
                        "date": "2020",
                    },
                    {
                        "amount": 0.0,
                        "percent": 0.0,
                        "item": "Governance, Administration, Planning and Development",
                        "date": "2020",
                    },
                    {
                        "amount": 7973764641.0,
                        "percent": 22.05,
                        "item": "Municipal governance and administration",
                        "date": "2020",
                    },
                    {
                        "amount": 381585830.0,
                        "percent": 1.06,
                        "item": "Other",
                        "date": "2020",
                    },
                    {
                        "amount": 16081731467.0,
                        "percent": 44.47,
                        "item": "Trading services",
                        "date": "2020",
                    },
                ]
            },
            result,
        )
