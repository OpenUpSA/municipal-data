from django.core.management.base import BaseCommand, CommandError
from scorecard.models import Geography
from infrastructure import utils
import os

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
        parser.add_argument('geography_code', type=str)
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        geo_code = options["geography_code"]
        filename = options["filename"]
        if Geography.objects.filter(geo_code=geo_code).count() == 0:
            raise CommandError("%s is an unknown Geography. Please ensure that this Geography exists in the database" % geo_code)
            
        geography = Geography.objects.get(geo_code=geo_code)

        if not os.path.exists(filename):
            raise CommandError("Can't file filename: %s" % filename)

        utils.load_file(geography, open(filename))
