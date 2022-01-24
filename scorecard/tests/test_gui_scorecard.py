from django.test import Client
from django.urls import reverse
from django.contrib.sites.models import Site
from django_q.models import OrmQ

from municipal_finance.tests.helpers import BaseSeleniumTestCase


class ScorecardTest(BaseSeleniumTestCase):
    fixtures = ["seeddata", "demo-data"]

    def setUp(self):
        super(ScorecardTest, self).setUp()
        
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')

    def test_quarterly_chart(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        self.wait_until_text_in(".page-heading__title", "Buffalo City")

        