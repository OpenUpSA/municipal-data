from collections import defaultdict
from django.conf import settings
from wazimap.data.tables import get_datatable
from wazimap.geo import geo_data
import json
import os

from scorecard.utils import comparison_relative_words

INDICATORS = [
    'cap_budget_diff',
    'cash_at_year_end',
    'cash_coverage',
    'current_debtors_collection_rate',
    'current_ratio',
    'liquidity_ratio',
    'op_budget_diff',
    'rep_maint_perc_ppe',
    'wasteful_exp',
]


def build_comparisons(geo, indicators, medians):
    # TODO: move the indicator metadata into the indicator calculator object itself
    build_comparison(geo, indicators, medians, "cash_at_year_end", "R", "cash balance")
    build_comparison(geo, indicators, medians, "cash_coverage", "months", "coverage")
    build_comparison(geo, indicators, medians, "op_budget_diff", "%", "underspending or overspending")
    build_comparison(geo, indicators, medians, "cap_budget_diff", "%", "underspending or overspending")
    build_comparison(geo, indicators, medians, "rep_maint_perc_ppe", "%", "spending")
    build_comparison(geo, indicators, medians, "wasteful_exp", "%", "expenditure")
    build_comparison(geo, indicators, medians, "current_ratio", "ratio", "ratio")
    build_comparison(geo, indicators, medians, "liquidity_ratio", "ratio", "ratio")
    build_comparison(geo, indicators, medians, "current_debtors_collection_rate", "%", "rate")


def build_comparison(geo, indicators, medians, indicator_name, result_type=None, noun='figure'):
    comparisons = {}

    for entry in indicators[indicator_name]['values']:
        val = entry['result']
        if val is None:
            continue

        date = str(entry['date'])
        comparisons[date] = [{
            # provincial median
            'type': 'relative',
            'place': 'similar municipalities in ' + geo.province_name,
            'value': medians[indicator_name]['provincial']['dev_cat'].get(date, 0),
            'value_type': result_type,
            'comparison': comparison_relative_words(val, medians[indicator_name]['provincial']['dev_cat'].get(date, 0), noun),
        }, {
            # national median
            'type': 'relative',
            'place': 'similar municipalities nationally',
            'value': medians[indicator_name]['national']['dev_cat'].get(date, 0),
            'value_type': result_type,
            'comparison': comparison_relative_words(val, medians[indicator_name]['national']['dev_cat'].get(date, 0), noun),
        }]

    indicators[indicator_name]['comparisons'] = comparisons


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
    for indicator in INDICATORS:
        medians[indicator]['national']['dev_cat'] = all_medians['national'][indicator][geo.miif_category]
        medians[indicator]['provincial']['dev_cat'] = all_medians['provincial'][indicator][geo.province_code][geo.miif_category]

    build_comparisons(geo, indicators, medians)

    profile.update({
        'total_population': total_pop,
        'population_density': population_density,
        'medians': medians,
    })
    return profile
