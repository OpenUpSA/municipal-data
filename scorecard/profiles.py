import requests
import json

API_URL = 'https://data.municipalmoney.org.za/api/cubes/'
Q4 = [10, 11, 12]
current_month = 12

def get_quarter_results(results, amount_field='amount.sum'):
    return sum([r[amount_field] for r in results['cells'] if r['financial_period.period'] in Q4 and r[amount_field]])

def get_profile(geo_code, geo_level, profile_name=None):

    api_query_string = '{cube}/aggregate?aggregates={aggregate}&cut=item.code:"{item_code}"|amount_type.label:"{amount_type}"|financial_year_end.year:{year}|demarcation.code:"{demarcation_code}"&drilldown=item.code|item.label|financial_period.period&page=0&pagesize=300000'


    ratio_items = {
        'operating_expenditure_actual': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'item_code': '4600',
            'amount_type': 'Actual',
            'year': '2015',
            'demarcation_code': geo_code,
        },
        'operating_expenditure_budgeted': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'item_code': '4600',
            'amount_type': 'Adjusted Budget',
            'year': '2015',
            'demarcation_code': geo_code,
        },
        'cash_flow': {
            'cube': 'cflow',
            'aggregate': 'amount.sum',
            'item_code': '4200',
            'amount_type': 'Actual',
            'year': '2015',
            'demarcation_code': geo_code,
        },
        'debtors': {
            'cube': 'aged_debtor',
            'aggregate': 'total_amount.sum',
            'item_code': '2600', # We should ideally be using 2000, but the numbers for it is incorrect at the moment.
            'amount_type': 'Actual',
            'year': '2015',
            'demarcation_code': geo_code,
        },
        'capital_revenue': {
            'cube': 'capital',
            'aggregate': 'asset_register_summary.sum',
            'item_code': '4100',
            'amount_type': 'Actual',
            'year': '2015',
            'demarcation_code': geo_code,
        },
        'operating_revenue': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'item_code': '2100',
            'amount_type': 'Actual',
            'year': '2015',
            'demarcation_code': geo_code,
        },
        'capital_grant': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'item_code': '1610',
            'amount_type': 'Actual',
            'year': '2015',
            'demarcation_code': geo_code,
        },
        'operating_grant': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'item_code': '1600',
            'amount_type': 'Actual',
            'year': '2015',
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
            # period_length=v['period_length'],
            demarcation_code=v['demarcation_code']
        )
        results[k] = requests.get(url, verify=False).json()

    operating_expenditure_actual = get_quarter_results(results['operating_expenditure_actual'])
    operating_expenditure_budgeted = results['operating_expenditure_budgeted']['cells'][0]['amount.sum']
    cash_flow = [r['amount.sum'] for r in results['cash_flow']['cells'] if r['financial_period.period'] == current_month][0]
    debtors = [r['total_amount.sum'] for r in results['debtors']['cells'] if r['financial_period.period'] == current_month][0]
    capital_revenue = get_quarter_results(results['capital_revenue'], ratio_items['capital_revenue']['aggregate'])
    operating_revenue = get_quarter_results(results['operating_revenue'])
    capital_grant = get_quarter_results(results['capital_grant'])
    operating_grant = get_quarter_results(results['operating_grant'])

    debtors_as_perc_of_revenue = debtors / ((capital_revenue + operating_revenue) - (capital_grant + operating_grant)) * 100
    cash_coverage = cash_flow / (operating_expenditure_actual / 12)
    operating_budget_diff = (operating_expenditure_actual - operating_expenditure_budgeted) / operating_expenditure_budgeted

    return {
        'cash_coverage': cash_coverage,
        'debtors_as_perc_of_revenue': debtors_as_perc_of_revenue,
        'operating_budget_diff': operating_budget_diff}
