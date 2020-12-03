from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import io
import PyPDF2
import tempfile


class PDFTests(StaticLiveServerTestCase):
    fixtures = ['tests/test_profile_and_pdf']
    port = 9000

    def test_pdf_download(self):
        response = self.client.get(f"{ self.live_server_url }/profiles/municipality-BUF-buffalo-city.pdf")
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(response.content)
        temp_file.flush()
        temp_file.seek(0)
        pdfReader = PyPDF2.PdfFileReader(temp_file)
        self.assertEqual(11, pdfReader.numPages)
        pageObj = pdfReader.getPage(0)
        print(pageObj.extractText())
        self.assertTrue("Buffalo City" in pageObj.extractText())
