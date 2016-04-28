import requests
import json

API_URL = 'https://data.municipalmoney.org.za/api/cubes/'
Q4 = [10, 11, 12]
current_month = 12

def get_quarter_results(results, amount_field='amount.sum'):
    return sum([r[amount_field] for r in results['cells'] if r['financial_period.period'] in Q4 and r[amount_field]])

def get_profile(geo_code, geo_level, profile_name=None):

    api_query_string = '{cube}/aggregate?aggregates={aggregate}&cut={cut}&drilldown=item.code|item.label|financial_period.period&page=0&pagesize=300000'

    line_items = {
        'op_exp_actual': {
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
        'op_exp_budget': {
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
        'cap_rev': {
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
        'op_rev': {
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
        'cap_grant': {
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
        'op_grant': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '1600',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        },
        'rep_maint': {
            'cube': 'repmaint',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '5005',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month'
            }
        },
        'ppe': {
            'cube': 'bsheet',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '1300',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month',
                'financial_period.period': current_month
            }
        },
        'invest_prop': {
            'cube': 'bsheet',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '1401',
                'amount_type.label': 'Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'month',
                'financial_period.period': current_month
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


    op_exp_actual = get_quarter_results(results['op_exp_actual'])
    op_exp_budget = results['op_exp_budget']['cells'][0]['amount.sum']
    op_rev = get_quarter_results(results['op_rev'])

    cap_exp_actual = get_quarter_results(
        results['cap_exp_actual'],
        line_items['cap_exp_actual']['aggregate'])
    cap_exp_budget = results['cap_exp_budget']['cells'][0][line_items['cap_exp_budget']['aggregate']]
    cap_rev = get_quarter_results(results['cap_rev'], line_items['cap_rev']['aggregate'])

    cash_flow = [
        r['amount.sum'] for r in results['cash_flow']['cells']
        if r['financial_period.period'] == current_month][0]

    debtors = [
        r['total_amount.sum'] for r in results['debtors']['cells']
        if r['financial_period.period'] == current_month][0]

    cap_grant = get_quarter_results(results['cap_grant'])
    op_grant = get_quarter_results(results['op_grant'])

    rep_maint = get_quarter_results(results['rep_maint']) or 0
    ppe = results['ppe']['cells'][0][line_items['ppe']['aggregate']] or 0
    invest_prop = results['invest_prop']['cells'][0][line_items['ppe']['aggregate']] or 0

    debtors_perc_rev = debtors / ((cap_rev+op_rev) - (cap_grant + op_grant)) * 100
    cash_coverage = cash_flow / (op_exp_actual / 12)
    op_budget_diff = (op_exp_actual - op_exp_budget) / op_exp_budget if op_exp_budget else 0
    cap_budget_diff = (cap_exp_actual - cap_exp_budget) / cap_exp_budget if cap_exp_budget else 0
    rep_maint_perc_ppe = rep_maint * 12 / (ppe + invest_prop)

    return {
        'cash_coverage': cash_coverage,
        'debtors_perc_rev': debtors_perc_rev,
        'op_budget_diff': op_budget_diff,
        'cap_budget_diff': cap_budget_diff,
        'rep_maint_perc_ppe': rep_maint_perc_ppe}
