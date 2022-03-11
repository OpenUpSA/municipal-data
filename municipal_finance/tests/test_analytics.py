from django.test import TestCase, override_settings
from django.conf import settings

class TestAnalytics(TestCase):

    @override_settings(NO_INDEX=False)
    def test_enable_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<meta name="robots" content="noindex">' not in str(response.content))
        self.assertTrue("noindex" not in str(response.content))

    @override_settings(NO_INDEX=True)
    def test_disable_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<meta name="robots" content="noindex">' in str(response.content))