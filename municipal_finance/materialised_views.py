"""
A script to build a set files of materialised views of the data presented
in municipality profiles on the Municipal Money website.

Municipality-specific profile data is stored in municipality-specific files
since producing them takes a lot of time with many queries against the API.
By storing municipality-specific data separately from comparisons to other
municipalities based on this data (e.g. medians, number of similar
municipalities in norm bounds) allows quick iteration on the latter without
recalculating muni-specifics from the API each time.

By storing this data to file instead of database, version control helps to
understand what changed as code is changed and avoid unintended changes to
calculations. It also allows deploying template and data changes synchronously
and avoids data/code structure mismatch that could occur if the data is in
a database and not upgraded during deployment - potentially leading to downtime.

By keeping this script separate from the Municipal Money website django app,
this data can be recalculated without more-complex environment setup.
"""
import json
import argparse
from scorecard.profile_data import (
    APIData,
    MuniApiClient,
    Demarcation,
    get_indicators,
    get_indicator_calculators,
)
from itertools import groupby
from collections import defaultdict
import sys
from .models import MunicipalityProfile


sys.path.append('.')


API_URL = 'https://municipaldata.treasury.gov.za/api'


def main():
    parser = argparse.ArgumentParser(
        description='Tool to dump the materialised views of the municipal finance data used on the Municipal Money website.')
    parser.add_argument(
        '--api-url',
        help='API URL to use. Default: ' + API_URL)
    command_group = parser.add_mutually_exclusive_group(required=True)
    command_group.add_argument(
        '--profiles-from-api',
        action='store_true',
        help='Fetch profile data from API, generate and store profiles.')
    command_group.add_argument(
        '--calc-medians',
        action='store_true',
        help='Calculate medians from stored profiles and store.')
    command_group.add_argument(
        '--calc-rating-counts',
        action='store_true',
        help='Calculate the number of items with each rating from stored profiles and store.')
    parser.add_argument(
        '--print-sets',
        action='store_true',
        help='Print the distribution sets')
    parser.add_argument(
        '--skip',
        nargs='?',
        default=0,
        help='The number of municipalities to skip')
    args = parser.parse_args()
    if args.api_url:
        api_url = args.api_url
    else:
        api_url = API_URL

    if args.profiles_from_api:
        generate_profiles(args, api_url)
    elif args.calc_medians:
        calculate_medians(args, api_url)
    elif args.calc_rating_counts:
        calculate_rating_counts(args, api_url)


def generate_profiles(args, api_url):
    api_client = MuniApiClient(api_url)
    munis = get_munis(api_client)
    for muni in munis[int(args.skip):]:
        demarcation_code = muni.get('municipality.demarcation_code')
        api_data = APIData(api_client.API_URL,
                           demarcation_code, client=api_client)
        api_data.fetch_data()
        indicators = get_indicators(api_data)
        profile = {
            'mayoral_staff': api_data.mayoral_staff(),
            'muni_contact': api_data.muni_contact(),
            'audit_opinions': api_data.audit_opinions(),
            'indicators': indicators,
            'demarcation': Demarcation(api_data).as_dict(),
        }
        # Save profile to database
        MunicipalityProfile(
            demarcation_code=demarcation_code,
            data=profile,
        ).save()


def calculate_medians(args, api_url):
    api_client = MuniApiClient(api_url)
    munis = get_munis(api_client)

    for muni in munis:
        demarcation_code = muni.get('municipality.demarcation_code')
        filename = "scorecard/materialised/profiles/%s.json" % demarcation_code
        with open(filename, 'r') as f:
            profile = json.load(f)
        indicators = profile['indicators']

        muni.update(indicators)

    nat_sets, nat_medians = calc_national_medians(munis)
    prov_sets, prov_medians = calc_provincial_medians(munis)

    if args.print_sets:
        print("Indicator value sets by MIIF category nationally")
        print(json.dumps(nat_sets, sort_keys=True,
                         indent=4, separators=(',', ': ')))
        print
        print("Indicator value sets by MIIF category and province")
        print(json.dumps(prov_sets, sort_keys=True,
                         indent=4, separators=(',', ': ')))

    # write medians
    filename = "scorecard/materialised/indicators/distribution/median.json"
    medians = {
        'provincial': prov_medians,
        'national': nat_medians,
    }
    with open(filename, 'w', encoding="utf8") as f:
        json.dump(medians, f, sort_keys=True, indent=4, separators=(',', ': '))


def calc_national_medians(munis):
    nat_sets = get_national_miif_sets(munis)
    nat_medians = defaultdict(lambda: defaultdict(dict))

    # calculate national median per MIIF category and year for each indicator
    for name in nat_sets.keys():
        for dev_cat in nat_sets[name].keys():
            for year in nat_sets[name][dev_cat].keys():
                results = [period['result']
                           for period in nat_sets[name][dev_cat][year]]
                nat_medians[name][dev_cat][year] = median(results)
    return nat_sets, nat_medians


def calc_provincial_medians(munis):
    prov_sets = get_provincial_miif_sets(munis)
    prov_medians = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    # calculate provincial median per province, MIIF category and year for each indicator
    for name in prov_sets.keys():
        for prov_code in prov_sets[name].keys():
            for dev_cat in prov_sets[name][prov_code].keys():
                for year in prov_sets[name][prov_code][dev_cat].keys():
                    results = [period['result']
                               for period in prov_sets[name][prov_code][dev_cat][year]]
                    prov_medians[name][prov_code][dev_cat][year] = median(
                        results)
    return prov_sets, prov_medians


def median(items):
    sorted_items = sorted(items)
    count = len(sorted_items)
    if count % 2 == 1:
        # middle item of odd set is floor of half of count
        return sorted_items[count//2]
    else:
        # middle item of even set is mean of middle two items
        return (sorted_items[(count-1)//2] + sorted_items[(count+1)//2])/2.0


def calculate_rating_counts(args, api_url):
    api_client = MuniApiClient(api_url)
    munis = get_munis(api_client)

    for muni in munis:
        demarcation_code = muni.get('municipality.demarcation_code')
        filename = "scorecard/materialised/profiles/%s.json" % demarcation_code
        with open(filename, 'r') as f:
            profile = json.load(f)
        indicators = profile['indicators']

        muni.update(indicators)

    nat_sets, nat_rating_counts = calc_national_rating_counts(munis)
    prov_sets, prov_rating_counts = calc_provincial_rating_counts(munis)

    if args.print_sets:
        print("Indicator value sets by MIIF category nationally")
        print(json.dumps(nat_sets, sort_keys=True,
                         indent=4, separators=(',', ': ')))
        print
        print("Indicator value sets by MIIF category and province")
        print(json.dumps(prov_sets, sort_keys=True,
                         indent=4, separators=(',', ': ')))

    # write rating counts
    filename = "scorecard/materialised/indicators/distribution/rating_counts.json"
    rating_counts = {
        'provincial': prov_rating_counts,
        'national': nat_rating_counts,
    }
    with open(filename, 'w', encoding="utf8") as f:
        json.dump(rating_counts, f, sort_keys=True,
                  indent=4, separators=(',', ': '))


def calc_national_rating_counts(munis):
    """
    Calculate the number of munis with each norm rating per MIIF category
    and year for each indicator
    """
    nat_sets = get_national_miif_sets(munis)
    nat_rating_counts = defaultdict(
        lambda: defaultdict(lambda: defaultdict(dict)))

    def rating_key(period): return period['rating']
    for name in nat_sets.keys():
        for dev_cat in nat_sets[name].keys():
            for year in nat_sets[name][dev_cat].keys():
                rating_sorted = sorted(
                    nat_sets[name][dev_cat][year], key=rating_key)
                for rating, rating_group in groupby(rating_sorted, rating_key):
                    nat_rating_counts[name][dev_cat][year][rating] = len(
                        list(rating_group))
    return nat_sets, nat_rating_counts


def calc_provincial_rating_counts(munis):
    """
    Calculate the number of munis with each norm rating per province,
    MIIF category and year for each indicator
    """
    prov_sets = get_provincial_miif_sets(munis)
    prov_rating_counts = defaultdict(lambda: defaultdict(
        lambda: defaultdict(lambda: defaultdict(dict))))

    def rating_key(period): return period['rating']
    for name in prov_sets.keys():
        for prov_code in prov_sets[name].keys():
            for dev_cat in prov_sets[name][prov_code].keys():
                for year in prov_sets[name][prov_code][dev_cat].keys():
                    rating_sorted = sorted(
                        prov_sets[name][prov_code][dev_cat][year], key=rating_key)
                    for rating, rating_group in groupby(rating_sorted, rating_key):
                        prov_rating_counts[name][prov_code][dev_cat][year][rating] = len(
                            list(rating_group))
    return prov_sets, prov_rating_counts


def get_national_miif_sets(munis):
    """
    collect set of indicator values for each MIIF category and year
    returns dict of the form {
      'cash_coverage': {
        'B1': {
          '2015': [{'result': ...}]
        }
      }
    }
    """
    nat_sets = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    def dev_cat_key(muni): return muni['municipality.miif_category']
    dev_cat_sorted = sorted(munis, key=dev_cat_key)
    for calculator in get_indicator_calculators(has_comparisons=True):
        name = calculator.indicator_name
        for dev_cat, dev_cat_group in groupby(dev_cat_sorted, dev_cat_key):
            for muni in dev_cat_group:
                for period in muni[name]['values']:
                    if period['result'] is not None:
                        nat_sets[name][dev_cat][period['date']].append(period)
    return nat_sets


def get_provincial_miif_sets(munis):
    """
    collect set of indicator values for each province, MIIF category and year
    returns dict of the form {
      'cash_coverage': {
        'FS': {
          'B1': {
            '2015': [{'result': ...}]
          }
        }
      }
    }
    """
    prov_sets = defaultdict(lambda: defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))))

    def dev_cat_key(muni): return muni['municipality.miif_category']
    dev_cat_sorted = sorted(munis, key=dev_cat_key)
    def prov_key(muni): return muni['municipality.province_code']
    for calculator in get_indicator_calculators(has_comparisons=True):
        name = calculator.indicator_name
        for dev_cat, dev_cat_group in groupby(dev_cat_sorted, dev_cat_key):
            prov_sorted = sorted(dev_cat_group, key=prov_key)
            for prov_code, prov_group in groupby(prov_sorted, prov_key):
                for muni in prov_group:
                    for period in muni[name]['values']:
                        if period['result'] is not None:
                            prov_sets[name][prov_code][dev_cat][period['date']].append(
                                period)
    return prov_sets


def get_munis(api_client):
    query = api_client.api_get({'query_type': 'facts',
                                'cube': 'municipalities',
                                'fields': [
                                    'municipality.demarcation_code',
                                    'municipality.name',
                                    'municipality.miif_category',
                                    'municipality.province_code',
                                ],
                                'value_label': '',
                                })
    result = query.result()
    result.raise_for_status()
    body = result.json()
    if body.get("total_cell_count") == body.get("page_size"):
        raise Exception("should page municipalities")
    return body.get("data")


if __name__ == "__main__":
    main()
