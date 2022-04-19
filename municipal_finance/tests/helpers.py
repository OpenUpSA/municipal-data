from datetime import datetime
from html.parser import HTMLParser
import unicodedata

from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
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

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_argument("--no-sandbox")
        d = DesiredCapabilities.CHROME
        d["loggingPrefs"] = {"browser": "ALL"}
        self.selenium = webdriver.Chrome(
            chrome_options=chrome_options, desired_capabilities=d
        )
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
