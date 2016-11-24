from wazimap.data.tables import get_datatable
from wazimap.geo import geo_data
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from profile_data import IndicatorCalculator
import json


def get_profile(geo_code, geo_level, profile_name=None):
    # Census data
    table = get_datatable('population_2011')
    _, total_pop = table.get_stat_data(geo_level, geo_code, percent=False)

    geo = geo_data.get_geography(geo_code, geo_level)
    population_density = None
    if geo.square_kms:
        population_density = total_pop / geo.square_kms

    filename = "indicators/municipality/%s.json" % geo_code
    with staticfiles_storage.open(filename) as f:
        indicators = json.load(f)

    indicator_calc = IndicatorCalculator(settings.API_URL_INTERNAL, geo_code)
    indicator_calc.fetch_data()

    return {
        'total_population': total_pop,
        'population_density': population_density,
        'mayoral_staff': indicator_calc.mayoral_staff(),
        'muni_contact': indicator_calc.muni_contact(),
        'audit_opinions': indicator_calc.audit_opinions(),
        'indicators': indicators,
    }
