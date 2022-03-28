from django.test import TestCase
from django.conf import settings


class TestNoIndex(TestCase):

    def test_indexing_is_allowed(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webflow/index.html')
        self.assertTrue('<meta name="robots" content="noindex">' not in str(response.content))
        self.assertTrue("noindex" not in str(response.content))

        response = self.client.get('/infrastructure/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'infrastructure/search.djhtml')
        self.assertTrue('<meta name="robots" content="noindex">' not in str(response.content))
        self.assertTrue("noindex" not in str(response.content))

    def test_indexing_is_blocked(self):
        settings.NO_INDEX = "env_bool"

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webflow/index.html')
        self.assertTrue('<meta name="robots" content="noindex">' in str(response.content))

        response = self.client.get('/infrastructure/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'infrastructure/search.djhtml')
        self.assertTrue('<meta name="robots" content="noindex">' in str(response.content))