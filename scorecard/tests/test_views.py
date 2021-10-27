import json

from django.test import (
    TransactionTestCase,
    Client,
    override_settings,
)

from . import (
    import_data,
)
from .resources import (
    GeographyResource,
    MunicipalityProfileResource,
    MedianGroupResource,
    RatingCountGroupResource,
)


@override_settings(
    SITE_ID=2,
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
)
class GeographyDetailViewTestCase(TransactionTestCase):
    serialized_rollback = True

    def test_context(self):
        # Import sample data
        import_data(
            GeographyResource,
            "views/scorecard_geography.csv",
        )
        import_data(
            MunicipalityProfileResource,
            "views/municipality_profile.csv",
        )
        import_data(
            MedianGroupResource,
            "views/median_group.csv",
        )
        import_data(
            RatingCountGroupResource,
            "views/rating_count_group.csv",
        )
        # Make request
        client = Client()
        response = client.get("/profiles/municipality-CPT-city-of-cape-town/")
        context = response.context
        page_data = json.loads(context["page_data_json"])
        # Test for amount types
        self.assertIsInstance(page_data["amount_types_v1"], dict)
        # Test for cube names
        self.assertIsInstance(page_data["cube_names"], dict)
        # Test for municipality category descriptions
        self.assertIsInstance(page_data["municipal_category_descriptions"], dict)
