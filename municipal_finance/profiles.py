import requests
import json

API_URL = 'http://data.municipalmoney.org.za/api/cubes/'
Q4 = [10, 11, 12]

def get_quarter_results(results, amount_field='amount.sum'):
    return sum([r[amount_field] for r in results['cells'] if r['financial_period.period'] in Q4])

def get_profile(geo_code, geo_level, profile_name=None):

    api_query_string = '{cube}/aggregate?aggregates={aggregate}&cut=item.code:"{item_code}"|amount_type.label:"{amount_type}"|financial_year_end.year:{year}|period_length.length:"{period_length}"|demarcation.code:"{demarcation_code}"&drilldown=item.code|item.label|financial_period.period&page=0&pagesize=300000'

    ratio_items = {
        'operating_expenditure_actual': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'item_code': '4600',
            'amount_type': 'Actual',
            'year': '2015',
            'period_length': 'month',
            'demarcation_code': geo_code,
        },
        'cash_flow': {
            'cube': 'cflow',
            'aggregate': 'amount.sum',
            'item_code': '4200',
            'amount_type': 'Actual',
            'year': '2015',
            'period_length': 'month',
            'demarcation_code': geo_code,
        }
    }

    results = {}
    for k, v in ratio_items.iteritems():
        url = API_URL + api_query_string.format(
            cube=v['cube'],
            aggregate=v['aggregate'],
            item_code=v['item_code'],
            amount_type=v['amount_type'],
            year=v['year'],
            period_length=v['period_length'],
            demarcation_code=v['demarcation_code']
        )
        results[k] = requests.get(url).json()

    operating_expenditure_actual = get_quarter_results(results['operating_expenditure_actual'])
    cash_flow = [r['amount.sum'] for r in results['cash_flow']['cells'] if r['financial_period.period'] == 12][0]

    cash_coverage = cash_flow / (operating_expenditure_actual / 4)

    return {'cash_coverage': cash_coverage}
