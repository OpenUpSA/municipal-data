from django.test import TestCase
from django.conf import settings


class TestAnalytics(TestCase):

    def test_noindex_flag(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<meta name="robots" content="noindex">' not in str(response.content))
        
        settings.NO_INDEX = "True"
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<meta name="robots" content="noindex">' in str(response.content))