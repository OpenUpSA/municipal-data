from django.test import TestCase

from scorecard.tests import import_data
from scorecard.tests.resources import (
    GeographyResource,
    MunicipalityProfileResource,
    MedianGroupResource,
    RatingCountGroupResource,
)

from site_config.models import SiteNotice


class TestSiteNotice(TestCase):
    fixtures = ["seeddata"]

    def setUp(self):
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

        SiteNotice.objects.create(description="Notice description", content="This is a test notice")

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("This is a test notice" in str(response.content))

    def test_help(self):
        response = self.client.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("This is a test notice" in str(response.content))

    def test_terms(self):
        response = self.client.get('/terms')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("This is a test notice" in str(response.content))

    def test_muni_scorecard(self):
        response = self.client.get('/profiles/municipality-CPT-city-of-cape-town/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("This is a test notice" in str(response.content))

    def test_infra_project_list(self):
        response = self.client.get('/infrastructure/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("This is a test notice" in str(response.content))