from collections import defaultdict
from django.conf import settings
from profile_data import get_indicator_calculators
from wazimap.data.tables import get_datatable
from wazimap.geo import geo_data
import json
import os

from scorecard.utils import comparison_relative_words


def get_profile(geo_code, geo_level, profile_name=None):
    # Census data
    table = get_datatable('population_2011')
    _, total_pop = table.get_stat_data(geo_level, geo_code, percent=False)

    geo = geo_data.get_geography(geo_code, geo_level)
    population_density = None
    if geo.square_kms:
        population_density = total_pop / geo.square_kms

    profile = get_precalculated_profile(geo_code)
    indicators = profile['indicators']
    medians = get_medians(geo)
    rating_counts = get_rating_counts(geo)
    build_comparisons(geo, indicators, medians, rating_counts)

    profile.update({
        'total_population': total_pop,
        'population_density': population_density,
        'medians': medians,
        'rating_counts': rating_counts,
    })
    return profile


def build_comparisons(geo, indicators, medians, rating_counts):
    for calculator in get_indicator_calculators(has_comparisons=True):
        build_comparison(geo, indicators, medians, rating_counts, calculator)


def build_comparison(geo, indicators, medians, rating_counts, calculator):
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


def get_precalculated_profile(geo_code):
    filename = os.path.join(
        settings.MATERIALISED_VIEWS_BASE,
        "profiles/%s.json" % geo_code)
    if not os.path.abspath(filename).startswith(settings.MATERIALISED_VIEWS_BASE):
        raise Exception("Trying to load file outside app path")
    with open(filename) as f:
        profile = json.load(f)
    return profile


def get_medians(geo):
    return get_muni_comparison(geo, "median.json")


def get_rating_counts(geo):
    return get_muni_comparison(geo, "rating_counts.json")


def get_muni_comparison(geo, filename):
    """
    Returns a dict with the national and provincial comparison data specific to
    this municipality's province and MIIF category
    """
    filename = os.path.join(
        settings.MATERIALISED_VIEWS_BASE,
        "indicators/distribution/%s" % filename)
    with open(filename) as f:
        all_groups = json.load(f)
    comparisons = defaultdict(lambda: defaultdict(dict))
    for calculator in get_indicator_calculators(has_comparisons=True):
        name = calculator.indicator_name
        national = all_groups['national'][name][geo.miif_category]
        comparisons[name]['national']['dev_cat'] = national
        provincial = all_groups['provincial'][name][geo.province_code][geo.miif_category]
        comparisons[name]['provincial']['dev_cat'] = provincial
    return comparisons
