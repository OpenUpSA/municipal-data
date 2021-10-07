import warnings
from datetime import datetime

from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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

        self.addCleanup(self.log_failure_details)
        self.addCleanup(self.selenium.quit)

    def log_failure_details(self):
        for method, error in self._outcome.errors:
            if error:
                print(f"### collecting data for {method} {error} {self.id()}")
                for entry in self.selenium.get_log("browser"):
                    print(entry)

                now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
                if not self.selenium.get_screenshot_as_file(f"{now}-{self.id()}.png"):
                    warnings.warn("Selenium screenshot failed")

    def wait_until_text_in(self, selector, text):
        self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text)
        )
