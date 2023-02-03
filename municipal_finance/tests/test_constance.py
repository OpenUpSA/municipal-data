from django.test import TestCase
from django.contrib.sites.models import Site
from constance.test import override_config

from municipal_finance.admin import CustomConfigForm

class TestConstance(TestCase):
    fixtures = ["seeddata", "demo-data"]

    def setUp(self):
        super(TestConstance, self).setUp()
        Site.objects.filter(id=2).update(
            domain="municipalmoney.org.za", name="Scorecard"
        )

    def test_default_config(self):
        form = CustomConfigForm(initial={})
        choices = form.fields["CAPITAL_PROJECT_SUMMARY_YEAR"].choices
        self.assertEqual(choices, [('2019/2020', '2019/2020'), ('2020/2021', '2020/2021')])
