import sys
sys.path.append('.')

import numpy as np

from scorecard.profile_data import MuniApiClient
import argparse
import copy
import csv
import json
from indicators import get_munis

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
    'revenue_breakdown',
    'revenue_sources',
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
    print(munis)




if __name__ == "__main__":
    main()
