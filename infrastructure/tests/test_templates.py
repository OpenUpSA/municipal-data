from django.test import TestCase
from infrastructure import utils
from infrastructure import models

class TestListPage(TestCase):
    @classmethod
    def setUp(cls):
        pass

    def test_all_projects_view(self):
        response = self.client.get('/infrastructure/projects')
        self.assertEqual(response.status_code, 200)

        js = response.json()
        self.assertEquals(len(js["results"]), 3)
