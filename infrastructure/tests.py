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
        rows = [
            "field1,field2,field3",
            "value1,value2,value3"
        ]

        return self.generate_data(rows)

    def generate_good_data(self, num_rows=1):
        rows = []
        headers = ",".join(utils.headers)

        rows.append(headers)

        for i in range(num_rows):
            row = ",".join(["x" for h in utils.headers[0:-2]]) + ",0,0"
            rows.append(row)

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
            fp = StringIO()
            fp.write(",".join(utils.headers) + "\n")
            fp.write(",".join(["x" for x in utils.headers]) + "\n")
            fp.seek(0)
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
        utils.load_file(geography, fp)
        self.assertEqual(models.Project.objects.count(), 3)

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
