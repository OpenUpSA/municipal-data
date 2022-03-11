from django.test import TestCase
from django.conf import settings


class TestNoIndex(TestCase):

    def test_noindex_base(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<meta name="robots" content="noindex">' not in str(response.content))
        self.assertTrue("noindex" not in str(response.content))

        settings.NO_INDEX = "env_bool"
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<meta name="robots" content="noindex">' in str(response.content))

    def test_noindex_infra_projects(self):
        response = self.client.get('/infrastructure/projects/')
        self.assertTemplateUsed(response, 'infrastructure/search.djhtml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<meta name="robots" content="noindex">' not in str(response.content))
        self.assertTrue("noindex" not in str(response.content))

        settings.NO_INDEX = "env_bool"
        response = self.client.get('/infrastructure/projects/')
        self.assertTemplateUsed(response, 'infrastructure/search.djhtml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<meta name="robots" content="noindex">' in str(response.content))