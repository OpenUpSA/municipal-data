from django.test import TestCase
import csv
from infrastructure import utils
from infrastructure import models
from scorecard.models import Geography
from io import StringIO

class ImportCSVTestCase(TestCase):

    @classmethod
    def setUp(cls):
        Geography.objects.create(geo_level="X", geo_code="geo_code", province_name="Western Cape", province_code="WC", category="A")

    def generate_data(self, rows):
        fp = StringIO()
        for row in rows:
            fp.write("%s\n" % row)
        fp.seek(0)

        return fp

    def generate_bad_data(self):
        additional_headers = ",".join([
            "Audited Outcome 2018/2019",
            "Full Year Forecast 2019/20",
            "Budget year 2020/21",
            "Budget year 2021/22",
            "Budget year 2022/23",
        ])

        additional_data = ",".join([str(i) for i in range(len(additional_headers))])

        rows = [
            ",".join("field%d" % i for i in range(len(utils.headers))) + additional_headers,
            ",".join("value%d" % i for i in range(len(utils.headers))) + additional_data,
        ]

        return self.generate_data(rows)

    def generate_good_data(self, num_rows=1):
        rows = []
        headers = ",".join(utils.headers)

        additional_headers = ",".join([
            "Audited Outcome 2018/2019",
            "Full Year Forecast 2019/20",
            "Budget year 2020/21",
            "Budget year 2021/22",
            "Budget year 2022/23",
        ])

        additional_data = ",".join([str(i) for i in range(len(additional_headers))])

        rows.append("%s,%s" % (headers, additional_headers))

        for i in range(num_rows):
            row = ",".join(["x" for h in utils.headers[0:-2]]) + ",0,0"
            rows.append("%s,%s" % (row, additional_data))

        return self.generate_data(rows)

    def generate_bad_coordinates(self, num_rows=1):
        rows = []
        headers = ",".join(utils.headers)

        rows.append(headers)

        for i in range(num_rows):
            row = ",".join(["x" for h in utils.headers[0:-2]]) + ",,"
            rows.append(row)

        return self.generate_data(rows)

    def test_check_file(self):

        fp = self.generate_bad_data()
        self.assertRaises(ValueError, utils.check_file, fp)

        try:
            fp = self.generate_good_data()
            utils.check_file(fp)
        except ValueError:
            assert False

    def test_load_file_with_bad_data(self):
        fp = self.generate_bad_data()
        geography = Geography.objects.all().first()

        self.assertRaises(ValueError, utils.load_file, geography, fp)

    def test_load_file(self):
        self.assertEqual(models.Project.objects.count(), 0)

        fp = self.generate_good_data()

        geography = Geography.objects.all().first()

        utils.load_file(geography, fp)
        self.assertEqual(models.Project.objects.count(), 1)
        project = models.Project.objects.all().first()

        for h in utils.headers:
            if h == "Type":
                h = "project_type"
            elif h == "GPS Longitude":
                h = "longitude"

            h = h.lower().replace(" ", "_").replace("-", "")
            if h in ["latitude", "longitude"]:
                h = h.replace("gps", "")
                self.assertEquals(getattr(project, h), 0)
            elif h == "gps_latitude":
                h = "latitude"
            else:
                self.assertEquals(getattr(project, h.lower()), "x")

        fp = self.generate_good_data(num_rows=2)
        rows = utils.load_file(geography, fp)
        self.assertEqual(models.Project.objects.count(), 3)
        self.assertEquals(rows, 2)

    def test_load_additional_fields(self):
        self.assertEquals(models.FinancialYear.objects.count(), 0)
        self.assertEquals(models.BudgetPhase.objects.count(), 0)

        fp = self.generate_good_data()

        geography = Geography.objects.all().first()

        utils.load_file(geography, fp)
        self.assertEquals(models.BudgetPhase.objects.count(), 3)
        self.assertEquals(models.FinancialYear.objects.count(), 5)

        years = models.FinancialYear.objects.all()
        self.assertEquals(years[0].budget_year, "2018/2019")
        self.assertEquals(years[1].budget_year, "2019/2020")
        self.assertEquals(years[2].budget_year, "2020/2021")
        self.assertEquals(years[3].budget_year, "2021/2022")
        self.assertEquals(years[4].budget_year, "2022/2023")

    def load_good_data(self):
        fp = self.generate_good_data()
        geography = Geography.objects.all().first()
        utils.load_file(geography, fp)

    def test_load_expenditure(self):
        self.assertEquals(models.Expenditure.objects.count(), 0)
        self.load_good_data()

        self.assertEquals(models.Expenditure.objects.count(), 5)
        expenditures = models.Expenditure.objects.all()
        self.assertEquals(expenditures[0].financial_year.budget_year, "2018/2019")
        self.assertEquals(expenditures[0].budget_phase.name, "Audited Outcome")

        self.assertEquals(expenditures[0].amount, 0)
        self.assertEquals(expenditures[1].amount, 1)
        self.assertEquals(expenditures[2].amount, 2)
        self.assertEquals(expenditures[3].amount, 3)
        self.assertEquals(expenditures[4].amount, 4)


    def test_load_file_with_bad_coordinates(self):
        geography = Geography.objects.all().first()
        fp = self.generate_bad_coordinates()
        utils.load_file(geography, fp)

        project = models.Project.objects.first()
        self.assertIsNone(project.latitude)
        self.assertIsNone(project.longitude)

    def test_float_or_none(self):
        r = utils.float_or_none("10.5")
        self.assertEquals(type(r), float)

        r = utils.float_or_none("")
        self.assertEquals(r, None)

    def test_parse_finance_phase(self):
        phase, year = utils.parse_finance_phase("Audited Outcome 2018/2019")

        self.assertEquals(year, "2018/2019")
        self.assertEquals(phase, "Audited Outcome")

        phase, year = utils.parse_finance_phase("This is a phase 2018/2019")
        self.assertEquals(phase, "This is a phase")

        phase, year = utils.parse_finance_phase("Audited Outcome 2018/19")
        self.assertEquals(year, "2018/2019")

        self.assertRaises(ValueError, utils.parse_finance_phase, "dfsdfsdf fsdfdfs")

    def test_create_finance_phase(self):
        self.assertEquals(models.FinancialYear.objects.count(), 0)
        self.assertEquals(models.BudgetPhase.objects.count(), 0)

        utils.create_finance_phase("Audited Outcome 2018/2019")

        self.assertEquals(models.FinancialYear.objects.count(), 1)
        year = models.FinancialYear.objects.all().first()
        self.assertEquals(year.budget_year, "2018/2019")

        self.assertEquals(models.BudgetPhase.objects.count(), 1)
        phase = models.BudgetPhase.objects.all().first()
        self.assertEquals(phase.name, "Audited Outcome")

        utils.create_finance_phase("Another Outcome 2018/2019")
        self.assertEquals(models.FinancialYear.objects.count(), 1)
        self.assertEquals(models.BudgetPhase.objects.count(), 2)

        utils.create_finance_phase("Another Outcome 2018/2019")
        self.assertEquals(models.BudgetPhase.objects.count(), 2)
