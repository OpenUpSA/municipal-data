from datetime import datetime
from html.parser import HTMLParser
import os
import sys
import tempfile
import unicodedata

from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import logging

logger = logging.Logger(__name__)


class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


class BaseSeleniumTestCase(LiveServerTestCase):
    def setUp(self):
        super(BaseSeleniumTestCase, self).setUp()

        home = os.environ.get("HOME", "")
        if not (home and os.access(home, os.W_OK)):
            os.environ["HOME"] = tempfile.mkdtemp()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        chrome_bin = os.environ.get("CHROME_BIN")
        if chrome_bin:
            chrome_options.binary_location = chrome_bin

        driver_log = os.path.join(tempfile.mkdtemp(), "chromedriver.log")
        try:
            self.selenium = webdriver.Chrome(
                options=chrome_options,
                service_args=["--verbose"],
                service_log_path=driver_log,
            )
        except Exception:
            try:
                with open(driver_log) as f:
                    sys.stderr.write(
                        "\n===== ChromeDriver verbose log =====\n"
                        + f.read()
                        + "\n===== end ChromeDriver log =====\n"
                    )
            except OSError:
                pass
            raise
        self.selenium.implicitly_wait(10)
        self.wait = WebDriverWait(self.selenium, 5)

        self.addCleanup(self.selenium.quit)

    def wait_until_text_in(self, selector, text):
        if self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text)):
            pass
        else:
            text_content = self.selenium.find_elements_by_css_selector(selector)[0].text
            logger.error("Element contents: %s" % text_content)

    def html_to_text(self, element_content):
        f = HTMLFilter()
        f.feed(element_content)
        return unicodedata.normalize("NFKD", f.text)

    def enter_text(self, selector, text):
        self.selenium.find_element_by_css_selector(selector).send_keys(text)

    def click(self, selector):
        self.selenium.find_element_by_css_selector(selector).click()

    def href_contains_url(self, selector, link):
        element = self.selenium.find_elements_by_css_selector(f"{selector} [href]")[0]
        self.assertEquals(element.get_attribute("href"), link)
