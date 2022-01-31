import json

from django.test import (
    TransactionTestCase,
    Client,
    override_settings,
)


@override_settings(
    SITE_ID=2,
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
)
class GeographyDetailViewTestCase(TransactionTestCase):
    serialized_rollback = True
    fixtures = ["seeddata", "demo-data", "compiled_profile"]

    def test_context(self):
        # Make request
        client = Client()
        response = client.get("/profiles/municipality-BUF-buffalo-city/")
        context = response.context
        page_data = json.loads(context["page_data_json"])
        # Test for amount types
        self.assertIsInstance(page_data["amount_types_v1"], dict)
        # Test for cube names
        self.assertIsInstance(page_data["cube_names"], dict)
        # Test for municipality category descriptions
        self.assertIsInstance(page_data["municipal_category_descriptions"], dict)
