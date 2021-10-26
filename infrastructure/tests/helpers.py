from datetime import datetime

from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from infrastructure.models import Expenditure, FinancialYear, BudgetPhase


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
        self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text)
        )

    def create_expenditure(self, amount, phase, year):
        budget_phase = BudgetPhase.objects.get(name=phase)
        financial_year = FinancialYear.objects.get_or_create(budget_year=year)

        expenditure = Expenditure.objects.create(
            project=self.project,
            budget_phase=budget_phase,
            financial_year=financial_year[0],
            amount=amount,
        )
        return expenditure