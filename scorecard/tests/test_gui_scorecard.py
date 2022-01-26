from django.test import Client
from django.urls import reverse
from django.contrib.sites.models import Site
from django_q.models import OrmQ

from municipal_finance.tests.helpers import BaseSeleniumTestCase


class ScorecardTest(BaseSeleniumTestCase):
    fixtures = ["demo-data", "seeddata", "cube-data"]

    def setUp(self):
        super(ScorecardTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')


    def test_scorecard_formula(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        self.wait_until_text_in("#cash-balance", "Cash Balance")
        self.wait_until_text_in(".indicator-detail", "Cash balance at the end of the financial year.")
        self.wait_until_text_in(".layout-grid__col--border-right", "Show calculation")
        #self.wait_until_text_in(".expand-block__content_inner", "Cash available at year end")