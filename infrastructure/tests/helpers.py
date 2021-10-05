"""
Common test helpers.
"""
import warnings
from datetime import datetime

from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core.management import call_command
from django.db import connections
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class WagtailHackMixin:

    def _fixture_teardown(self):
        # Allow TRUNCATE ... CASCADE and don't emit the post_migrate signal
        # when flushing only a subset of the apps
        for db_name in self._databases_names(include_mirrors=False):
            # Flush the database
            inhibit_post_migrate = (
                self.available_apps is not None
                or (  # Inhibit the post_migrate signal when using serialized
                    # rollback to avoid trying to recreate the serialized data.
                    self.serialized_rollback
                    and hasattr(connections[db_name], "_test_serialized_contents")
                )
            )
            call_command(
                "flush",
                verbosity=0,
                interactive=False,
                database=db_name,
                reset_sequences=False,
                allow_cascade=True,
                inhibit_post_migrate=inhibit_post_migrate,
            )


class BaseSeleniumTestCase(WagtailHackMixin, LiveServerTestCase):
    """
    Base class for Selenium tests.
    This saves a screenshot to the current directory on test failure.
    """

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
