import requests
import json

API_URL = 'https://data.municipalmoney.org.za/api/cubes/'
Q4 = [10, 11, 12]
current_month = 12

def get_quarter_results(results, amount_field='amount.sum'):
    return sum([r[amount_field] for r in results['cells'] if r['financial_period.period'] in Q4 and r[amount_field]])

def get_profile(geo_code, geo_level, profile_name=None):

    api_query_string = '{cube}/aggregate?aggregates={aggregate}&cut={cut}&drilldown=item.code|item.label|financial_period.period&page=0&pagesize=300000'

    # item.code:"{item_code}"|amount_type.label:"{amount_type}"|financial_year_end.year:{year}|demarcation.code:"{demarcation_code}"|period_length.length:"{period_length}"

    line_items = {
        'operating_expenditure_actual': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '4600',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        },
        'operating_expenditure_budgeted': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '4600',
                'amount_type.label': 'Adjusted Budget',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
            }
        },
        'cash_flow': {
            'cube': 'cflow',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '4200',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        },
        'debtors': {
            'cube': 'aged_debtor',
            'aggregate': 'total_amount.sum',
            'cut': {
                'item.code': '2600', # We should ideally be using 2000, but the numbers for it is incorrect at the moment.
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        },
        'capital_revenue': {
            'cube': 'capital',
            'aggregate': 'asset_register_summary.sum',
            'cut': {
                'item.code': '5100',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        },
        'cap_exp_actual': {
            'cube': 'capital',
            'aggregate': 'asset_register_summary.sum',
            'cut': {
                'item.code': '4100',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        },
        'cap_exp_budget': {
            'cube': 'capital',
            'aggregate': 'asset_register_summary.sum',
            'cut': {
                'item.code': '4100',
                'amount_type.label': 'Adjusted Budget',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
            }
        },
        'operating_revenue': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '2100',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        },
        'capital_grant': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '1610',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        },
        'operating_grant': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '1600',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        }
    }

    results = {}
    for item, details in line_items.iteritems():
        url = API_URL + api_query_string.format(
            cube=details['cube'],
            aggregate=details['aggregate'],
            cut='|'.join('{!s}:{!r}'.format(k, v) for (k, v) in details['cut'].iteritems()).replace("'", '"')
        )
        results[item] = requests.get(url, verify=False).json()

    operating_expenditure_actual = get_quarter_results(results['operating_expenditure_actual'])
    operating_expenditure_budgeted = results['operating_expenditure_budgeted']['cells'][0]['amount.sum']
    operating_revenue = get_quarter_results(results['operating_revenue'])

    cash_flow = [r['amount.sum'] for r in results['cash_flow']['cells'] if r['financial_period.period'] == current_month][0]
    debtors = [r['total_amount.sum'] for r in results['debtors']['cells'] if r['financial_period.period'] == current_month][0]

    cap_exp_actual = get_quarter_results(results['cap_exp_actual'], line_items['cap_exp_actual']['aggregate'])
    cap_exp_budget = results['cap_exp_budget']['cells'][0][line_items['cap_exp_budget']['aggregate']]
    capital_revenue = get_quarter_results(results['capital_revenue'], line_items['capital_revenue']['aggregate'])

    capital_grant = get_quarter_results(results['capital_grant'])
    operating_grant = get_quarter_results(results['operating_grant'])

    debtors_as_perc_of_revenue = debtors / ((capital_revenue + operating_revenue) - (capital_grant + operating_grant)) * 100
    cash_coverage = cash_flow / (operating_expenditure_actual / 12)
    operating_budget_diff = (operating_expenditure_actual - operating_expenditure_budgeted) / operating_expenditure_budgeted
    cap_budget_diff = (cap_exp_actual - cap_exp_budget) / cap_exp_budget if cap_exp_budget else 0

    return {
        'cash_coverage': cash_coverage,
        'debtors_as_perc_of_revenue': debtors_as_perc_of_revenue,
        'operating_budget_diff': operating_budget_diff,
        'cap_budget_diff': cap_budget_diff}
