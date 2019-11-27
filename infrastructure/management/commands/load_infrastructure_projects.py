from django.core.management.base import BaseCommand, CommandError
from scorecard.models import Geography
from infrastructure import utils
import os
import logging

logger = logging.Logger(__name__)

class Command(BaseCommand):
    help = """
        Load infrastructure projects from a csv file. The following headers are expected:
            Function,
            Project Decription,
            Project Number,
            Type,
            MTSF Service Outcome,
            IUDF,
            Own Strategic Objectives,
            Asset Class,
            Asset Sub-Class,
            Ward Location,
            GPS Longitude,
            GPS Latitude
    """

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)
        parser.add_argument('--geography_code', type=str, help="Municipal Code e.g. ETH, WC011, etc. The filename is used if this is not provided")

    def process_csv(self, filename, geo_code):
        if Geography.objects.filter(geo_code=geo_code).count() == 0:
            raise CommandError("%s is an unknown Geography. Please ensure that this Geography exists in the database" % geo_code)
        geography = Geography.objects.get(geo_code=geo_code)
        utils.load_csv(geography, open(filename))

    def handle(self, *args, **options):
        filename = options["filename"]
        geo_code = options["geography_code"]

        if not os.path.exists(filename):
            raise CommandError("Can't file filename: %s" % filename)

        if filename.endswith(".csv"):
            logging.info("Processing capital file as csv")
            if geo_code is None:
                basename = os.path.basename(filename)
                geo_code = basename.split(os.path.extsep)[0]
                logging.info("Municipal Code not provided, using filename: %s" % geo_code)
            self.process_csv(filename, geo_code)
        elif filename.endswith("xls") or filename.endswith("xlsx"):
            utils.load_excel(filename)

