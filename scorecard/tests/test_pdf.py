from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import io

class PDFTests(StaticLiveServerTestCase):
    fixtures = ['tests/test_profile_and_pdf']

    def test_pdf_download(self):
        response = self.client.get("/profiles/municipality-BUF-buffalo-city/")
        f = io.BytesIO(response.content)
