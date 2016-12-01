from collections import defaultdict
from django.conf import settings
from profile_data import get_indicator_calculators
from wazimap.data.tables import get_datatable
from wazimap.geo import geo_data
import json
import os

from scorecard.utils import comparison_relative_words


def build_comparisons(geo, indicators, medians):
    for calculator in get_indicator_calculators(has_comparisons=True):
        build_comparison(geo, indicators, medians, calculator)


def build_comparison(geo, indicators, medians, calculator):
    comparisons = {}

    for entry in indicators[calculator.indicator_name]['values']:
        val = entry['result']
        if val is None:
            continue

        date = str(entry['date'])
        comparisons[date] = [{
            # provincial median
            'type': 'relative',
            'place': 'similar municipalities in ' + geo.province_name,
            'value': medians[calculator.indicator_name]['provincial']['dev_cat'].get(date, 0),
            'value_type': calculator.result_type,
            'comparison': comparison_relative_words(val, medians[calculator.indicator_name]['provincial']['dev_cat'].get(date, 0), calculator.noun),
        }, {
            # national median
            'type': 'relative',
            'place': 'similar municipalities nationally',
            'value': medians[calculator.indicator_name]['national']['dev_cat'].get(date, 0),
            'value_type': calculator.result_type,
            'comparison': comparison_relative_words(val, medians[calculator.indicator_name]['national']['dev_cat'].get(date, 0), calculator.noun),
        }]

    indicators[calculator.indicator_name]['comparisons'] = comparisons


def get_profile(geo_code, geo_level, profile_name=None):
    # Census data
    table = get_datatable('population_2011')
    _, total_pop = table.get_stat_data(geo_level, geo_code, percent=False)

    geo = geo_data.get_geography(geo_code, geo_level)
    population_density = None
    if geo.square_kms:
        population_density = total_pop / geo.square_kms

    filename = os.path.join(
        settings.MATERIALISED_VIEWS_BASE,
        "profiles/%s.json" % geo_code)
    with open(filename) as f:
        profile = json.load(f)
    indicators = profile['indicators']

    filename = os.path.join(
        settings.MATERIALISED_VIEWS_BASE,
        "indicators/distribution/median.json")
    with open(filename) as f:
        all_medians = json.load(f)
    medians = defaultdict(lambda: defaultdict(dict))
    for calculator in get_indicator_calculators(has_comparisons=True):
        medians[calculator.indicator_name]['national']['dev_cat'] = all_medians['national'][calculator.indicator_name][geo.miif_category]
        medians[calculator.indicator_name]['provincial']['dev_cat'] = all_medians['provincial'][calculator.indicator_name][geo.province_code][geo.miif_category]

    build_comparisons(geo, indicators, medians)

    profile.update({
        'total_population': total_pop,
        'population_density': population_density,
        'medians': medians,
    })
    return profile
