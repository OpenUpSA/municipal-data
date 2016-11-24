import sys
sys.path.append('.')

import numpy as np

from scorecard.profile_data import MuniApiClient
import argparse
import json
from indicators import get_munis
from collections import defaultdict
from itertools import groupby

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
    parser = argparse.ArgumentParser(description='Tool to dump the materialised views of the municipal finance data used on the Municipal Money website.')
    parser.add_argument('--api-url', help='API URL to use. Default: ' + API_URL)

    args = parser.parse_args()
    if args.api_url:
        api_url = args.api_url
    else:
        api_url = API_URL

    api_client = MuniApiClient(api_url)

    munis = get_munis(api_client)

    for muni in munis:
        demarcation_code = muni.get('municipality.demarcation_code')
        filename = "scorecard/static/indicators/municipality/%s.json" % demarcation_code
        with open(filename, 'rd') as f:
            indicators = json.load(f)

        muni.update(indicators)

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

    # calculate national-indicator-development_category-year medians
    for indicator in nat_sets.keys():
        for dev_cat in nat_sets[indicator].keys():
            for year in nat_sets[indicator][dev_cat].keys():
                nat_medians[indicator][dev_cat][year] = median(nat_sets[indicator][dev_cat][year])

    # write medians
    filename = "scorecard/static/indicators/distribution/median.json"
    with open(filename, 'wb') as f:
        json.dump(nat_medians, f, sort_keys=True, indent=4, separators=(',', ': '))



def median(items):
    sorted_items = sorted(items)
    count = len(sorted_items)
    if count % 2 == 1:
        # middle item of odd set is floor of half of count
        return sorted_items[count/2]
    else:
        # middle item of even set is mean of middle two items
        return (sorted_items[(count-1)/2] + sorted_items[(count+1)/2])/2.0






if __name__ == "__main__":
    main()
