import json
from infrastructure.models import FinancialYear

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

        fy = FinancialYear.objects.create(budget_year="2019/2020")

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


class IndexViewTestCase(TransactionTestCase):
    serialized_rollback = True

    def test_metatags(self):
        client = Client()
        response = client.get("/")

        self.assertIn("<title>Municipal Money</title>", str(response.content))
        self.assertIn(
            '<meta content="An initiative of the National Treasury, which has collected extensive municipal financial data over several years and aims to share it with the public." name="description">',
            str(response.content),
        )
        self.assertIn(
            '<meta content="Municipal Money" property="og:title">',
            str(response.content),
        )
        self.assertIn(
            '<meta content="An initiative of the National Treasury, which has collected extensive municipal financial data over several years and aims to share it with the public." property="og:description">',
            str(response.content),
        )
        self.assertIn(
            '<meta content="Municipal Money" property="twitter:title">',
            str(response.content),
        )
        self.assertIn(
            '<meta content="An initiative of the National Treasury, which has collected extensive municipal financial data over several years and aims to share it with the public." property="twitter:description">',
            str(response.content),
        )
        self.assertIn(
            '<meta property="og:type" content="website">', str(response.content)
        )
        self.assertIn(
            '<meta content="summary" name="twitter:card">', str(response.content)
        )
