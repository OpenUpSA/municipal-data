import sys
sys.path.append('.')

import numpy as np

from scorecard.profile_data import MuniApiClient
import argparse
import json
from indicators import get_munis
from collections import defaultdict
from pprint import pprint

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


    sets = defaultdict(lambda: defaultdict(list))
    medians = defaultdict(dict)

    # collect indicator year sets
    for indicator in INDICATORS:
        for muni in munis:
            for period in muni[indicator]['values']:
                if period['result'] is not None:
                    sets[indicator][period['date']].append(period['result'])

    # calculate indicator-year medians
    for indicator in sets.keys():
        for year in sets[indicator].keys():
            medians[indicator][year] = median(sets[indicator][year])

    # write indicator-year medians
    for indicator in medians.keys():
        filename = "scorecard/static/indicators/distribution/median/indicator/%s.json" % indicator
        with open(filename, 'wb') as f:
            json.dump(medians[indicator], f, sort_keys=True, indent=4, separators=(',', ': '))



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
