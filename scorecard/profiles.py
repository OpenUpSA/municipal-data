import requests
import json

from wazimap.data.utils import percent, ratio

API_URL = 'https://data.municipalmoney.org.za/api/cubes/'
Q4 = [10, 11, 12]
current_month = 12

def get_quarter_results(results, amount_field='amount.sum'):
    return sum([r[amount_field] for r in results['cells'] if r['financial_period.period'] in Q4 and r[amount_field]])

def amount_from_results(item, results, line_items):
    """
    Returns the summed value from the results we received from the API.
    If the 'cells' list in the results is empty, no value was returned,
    and for now, we return zero in that case.
    We should be returning None, and checking for None values in the ratio calculation.
    """
    try:
        return results[item]['cells'][0][line_items[item]['aggregate']]
    except IndexError:
        return 0


def get_profile(geo_code, geo_level, profile_name=None):

    api_query_string = '{cube}/aggregate?aggregates={aggregate}&cut={cut}&drilldown=item.code|item.label|financial_period.period&page=0&pagesize=300000'

    line_items = {
        'op_exp_actual': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '4600',
                'amount_type.label': 'Audited Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'year'
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
                'amount_type.label': 'Audited Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'year'
            }
        },
        'cap_exp_actual': {
            'cube': 'capital',
            'aggregate': 'asset_register_summary.sum',
            'cut': {
                'item.code': '4100',
                'amount_type.label': 'Audited Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'year'
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
        'rep_maint': {
            'cube': 'repmaint',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '5005',
                'amount_type.label': 'Audited Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'year'
            }
        },
        'ppe': {
            'cube': 'bsheet',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '1300',
                'amount_type.label': 'Audited Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'year',
            }
        },
        'invest_prop': {
            'cube': 'bsheet',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '1401',
                'amount_type.label': 'Audited Actual',
                'financial_year_end.year': 2015,
                'demarcation.code': str(geo_code),
                'period_length.length': 'year',
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


    op_exp_actual = amount_from_results('op_exp_actual', results, line_items)
    op_exp_budget = amount_from_results('op_exp_budget', results, line_items)

    cap_exp_actual = amount_from_results('cap_exp_actual', results, line_items)
    cap_exp_budget = amount_from_results('cap_exp_budget', results, line_items)

    cash_flow = amount_from_results('cash_flow', results, line_items)

    rep_maint = amount_from_results('rep_maint', results, line_items)
    ppe = amount_from_results('ppe', results, line_items)
    invest_prop = amount_from_results('invest_prop', results, line_items)

    cash_coverage = ratio(cash_flow, (op_exp_actual / 12), 1)
    op_budget_diff = percent((op_exp_actual - op_exp_budget), op_exp_budget, 1)
    cap_budget_diff = percent((cap_exp_actual - cap_exp_budget), cap_exp_budget)
    rep_maint_perc_ppe = percent(rep_maint, (ppe + invest_prop))

    return {
        'cash_coverage': cash_coverage,
        'op_budget_diff': op_budget_diff,
        'cap_budget_diff': cap_budget_diff,
        'rep_maint_perc_ppe': rep_maint_perc_ppe}
