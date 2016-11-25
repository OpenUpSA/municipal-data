import sys
sys.path.append('.')

from collections import defaultdict
from itertools import groupby
from scorecard.profile_data import IndicatorCalculator, MuniApiClient
import argparse
import json

API_URL = 'https://municipaldata.treasury.gov.za/api'
INDICATORS = [
    'cap_budget_diff',
    'cash_at_year_end',
    'cash_coverage',
    'current_debtors_collection_rate',
    'current_ratio',
    'liquidity_ratio',
    'op_budget_diff',
    'rep_maint_perc_ppe',
    'wasteful_exp'
]


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
    parser.add_argument(
        '--print-sets',
        action='store_true',
        help='Print the distribution sets')
    args = parser.parse_args()
    if args.api_url:
        api_url = args.api_url
    else:
        api_url = API_URL

    if args.profiles_from_api:
        generate_profiles(api_url)
    elif args.calc_medians:
        calculate_medians(args, api_url)


def generate_profiles(api_url):
    api_client = MuniApiClient(api_url)
    munis = get_munis(api_client)

    for muni in munis:
        demarcation_code = muni.get('municipality.demarcation_code')
        indicator_calc = IndicatorCalculator(api_client.API_URL, demarcation_code, client=api_client)
        indicator_calc.fetch_data()
        indicators = indicator_calc.get_indicators()
        profile = {
            'mayoral_staff': indicator_calc.mayoral_staff(),
            'muni_contact': indicator_calc.muni_contact(),
            'audit_opinions': indicator_calc.audit_opinions(),
            'indicators': indicators,
        }

        filename = "scorecard/materialised/profiles/%s.json" % demarcation_code
        with open(filename, 'wb') as f:
            json.dump(profile, f, sort_keys=True, indent=4, separators=(',', ': '))


def calculate_medians(args, api_url):
    api_client = MuniApiClient(api_url)
    munis = get_munis(api_client)

    for muni in munis:
        demarcation_code = muni.get('municipality.demarcation_code')
        filename = "scorecard/materialised/profiles/%s.json" % demarcation_code
        with open(filename, 'rd') as f:
            profile = json.load(f)
        indicators = profile['indicators']

        muni.update(indicators)

    nat_sets, nat_medians = calc_national_sets(munis)
    prov_sets, prov_medians = calc_provincial_medians(munis)

    if args.print_sets:
        print("Indicator value sets by MIIF category nationally")
        print(json.dumps(nat_sets, sort_keys=True, indent=4, separators=(',', ': ')))
        print
        print("Indicator value sets by MIIF category and province")
        print(json.dumps(prov_sets, sort_keys=True, indent=4, separators=(',', ': ')))

    # write medians
    filename = "scorecard/materialised/indicators/distribution/median.json"
    medians = {
        'provincial': prov_medians,
        'national': nat_medians,
    }
    with open(filename, 'wb') as f:
        json.dump(medians, f, sort_keys=True, indent=4, separators=(',', ': '))


def calc_national_sets(munis):
    nat_sets = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    nat_medians = defaultdict(lambda: defaultdict(dict))

    # collect national-indicator-development_category-year sets
    dev_cat_key = lambda muni: muni['municipality.development_category']
    dev_cat_sorted = sorted(munis, key=dev_cat_key)
    for indicator in INDICATORS:
        for dev_cat, dev_cat_group in groupby(dev_cat_sorted, dev_cat_key):
            for muni in dev_cat_group:
                for period in muni[indicator]['values']:
                    if period['result'] is not None:
                        nat_sets[indicator][dev_cat][period['date']].append(period['result'])

    # calculate provincial-indicator-development_category-year medians
    for indicator in nat_sets.keys():
        for dev_cat in nat_sets[indicator].keys():
            for year in nat_sets[indicator][dev_cat].keys():
                nat_medians[indicator][dev_cat][year] = median(nat_sets[indicator][dev_cat][year])
    return nat_sets, nat_medians


def calc_provincial_medians(munis):
    prov_sets = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    prov_medians = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    # collect provincial-indicator-development_category-year sets
    dev_cat_key = lambda muni: muni['municipality.development_category']
    dev_cat_sorted = sorted(munis, key=dev_cat_key)
    prov_key = lambda muni: muni['municipality.province_code']
    for indicator in INDICATORS:
        for dev_cat, dev_cat_group in groupby(dev_cat_sorted, dev_cat_key):
            prov_sorted = sorted(dev_cat_group, key=prov_key)
            for prov_code, prov_group in groupby(prov_sorted, prov_key):
                for muni in prov_group:
                    for period in muni[indicator]['values']:
                        if period['result'] is not None:
                            prov_sets[indicator][prov_code][dev_cat][period['date']].append(period['result'])

    # calculate national-indicator-development_category-year medians
    for indicator in prov_sets.keys():
        for prov_code in prov_sets[indicator].keys():
            for dev_cat in prov_sets[indicator][prov_code].keys():
                for year in prov_sets[indicator][prov_code][dev_cat].keys():
                    prov_medians[indicator][prov_code][dev_cat][year] = median(prov_sets[indicator][prov_code][dev_cat][year])
    return prov_sets, prov_medians


def median(items):
    sorted_items = sorted(items)
    count = len(sorted_items)
    if count % 2 == 1:
        # middle item of odd set is floor of half of count
        return sorted_items[count/2]
    else:
        # middle item of even set is mean of middle two items
        return (sorted_items[(count-1)/2] + sorted_items[(count+1)/2])/2.0


def get_munis(api_client):
    query = api_client.api_get({'query_type': 'facts',
                                 'cube': 'municipalities',
                                 'fields': [
                                     'municipality.demarcation_code',
                                     'municipality.name',
                                     'municipality.development_category',
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
