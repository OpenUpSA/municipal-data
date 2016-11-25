import sys
sys.path.append('.')

from scorecard.profile_data import IndicatorCalculator, MuniApiClient
import argparse
import copy
import csv
import json

API_URL = 'https://municipaldata.treasury.gov.za/api'

def main():

    parser = argparse.ArgumentParser(description='Tool to dump the materialised views of the municipal finance data used on the Municipal Money website.')
    parser.add_argument('--api-url', help='API URL to use. Default: ' + API_URL)
    parser.add_argument('--write-csv', help='Write indicator values to dedicated CSV files in the current working directory', action='store_true')

    args = parser.parse_args()
    if args.api_url:
        api_url = args.api_url
    else:
        api_url = API_URL

    write_static = not args.write_csv

    api_client = MuniApiClient(api_url)

    munis = get_munis(api_client)

    for muni in munis:
        demarcation_code = muni.get('municipality.demarcation_code')
        indicator_calc = IndicatorCalculator(api_client.API_URL, demarcation_code, client=api_client)
        indicator_calc.fetch_data()
        indicators = indicator_calc.get_indicators()
        if write_static:
            filename = "scorecard/materialised/indicators/municipality/%s.json" % demarcation_code
            with open(filename, 'wb') as f:
                json.dump(indicators, f, sort_keys=True, indent=4, separators=(',', ': '))
        muni.update(indicators)

    if args.write_csv:
        write_csvs(munis)


def write_csvs(munis):
    indicators = munis[0]['indicators'].keys()
    for indicator in indicators:
        if munis[0]['indicators'][indicator].get('values'):
            example_value = munis[0]['indicators'][indicator]['values'][0]
            fieldnames = ['demarcation_code', 'development_category'] + example_value.keys()
            with open(indicator + '.csv', 'w') as file:
                writer = csv.DictWriter(file, fieldnames)
                writer.writeheader()

                for muni in munis:
                    values = copy.copy(muni['indicators'][indicator]['values'])
                    for value in values:
                        value['demarcation_code'] = muni['municipality.demarcation_code']
                        value['development_category'] = muni['municipality.development_category']
                        writer.writerow(value)


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
