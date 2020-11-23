from django.test import TransactionTestCase, override_settings

from municipal_finance.cubes import get_manager
from municipal_finance.resources import (
    CashflowFactsV1Resource,
    CashflowFactsV2Resource,
)

from ...resources import GeographyResource
from ...profile_data import (
    ApiClient,
    ApiData,
    CashBalance,
)

from .utils import (
    import_data,
    DjangoConnectionThreadPoolExecutor,
)


@override_settings(
    SITE_ID=3,
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
)
class TestCashBalance(TransactionTestCase):
    serialized_rollback = True

    def tearDown(self):
        get_manager().engine.dispose()

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'cash_balance/scorecard_geography.csv'
        )
        import_data(
            CashflowFactsV1Resource,
            'cash_balance/cash_flow_facts_v1.csv'
        )
        import_data(
            CashflowFactsV2Resource,
            'cash_balance/cash_flow_facts_v2.csv'
        )
        # Setup the API client
        executor = DjangoConnectionThreadPoolExecutor(max_workers=1)
        client = ApiClient(
            lambda u, p: executor.submit(self.client.get, u, data=p),
            "/api"
        )
        # Fetch data from API
        api_data = ApiData(client, "CPT")
        api_data.fetch_data([
            "cash_flow_v1",
            "cash_flow_v2",
        ])
        # Provide data to indicator
        result = CashBalance.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "values": [
                    {
                        "date": 2019,
                        "result": 7101183182,
                        "rating": "good"
                    },
                    {
                        "date": 2018,
                        "result": -3448597019,
                        "rating": "bad"
                    },
                    {
                        "date": 2017,
                        "result": 3773576000,
                        "rating": "good"
                    },
                    {
                        "date": 2016,
                        "result": 3803924000,
                        "rating": "good"
                    }
                ],
                "ref": {
                    "title": "State of Local Government Finances",
                    "url": "http://mfma.treasury.gov.za/Media_Releases/The%20state%20of%20local%20government%20finances/Pages/default.aspx"
                }
            }
        )
