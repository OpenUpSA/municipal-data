import requests
import json

from wazimap.data.utils import percent, ratio

API_URL = 'https://data.municipalmoney.org.za/api/cubes/'
YEARS = [2015, 2014, 2013, 2012, 2011]

def amount_from_results(item, year, results, line_items):
    """
    Returns the aggregated values we received from the API for the specified year.
    If the 'cells' list in the results is empty, no values were returned,
    and for now, we return zero in that case.
    We should be returning None, and checking for None values in the ratio calculation.
    """
    for cell in results[item]['cells']:
        if cell['financial_period.period'] == year:
            return cell[line_items[item]['aggregate']]
    return 0


def get_profile(geo_code, geo_level, profile_name=None):

    api_query_string = '{cube}/aggregate?aggregates={aggregate}&cut={cut}&drilldown=item.code|item.label|financial_period.period&page=0'

    line_items = {
        'op_exp_actual': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '4600',
                'amount_type.label': 'Audited Actual',
                'demarcation.code': str(geo_code),
                'period_length.length': 'year',
            },
            'results': {}
        },
        'op_exp_budget': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '4600',
                'amount_type.label': 'Adjusted Budget',
                'demarcation.code': str(geo_code),
            },
            'results': {}
        },
        'cash_flow': {
            'cube': 'cflow',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '4200',
                'amount_type.label': 'Audited Actual',
                'demarcation.code': str(geo_code),
                'period_length.length': 'year'
            },
            'results': {}
        },
        'cap_exp_actual': {
            'cube': 'capital',
            'aggregate': 'asset_register_summary.sum',
            'cut': {
                'item.code': '4100',
                'amount_type.label': 'Audited Actual',
                'demarcation.code': str(geo_code),
                'period_length.length': 'year'
            },
            'results': {}
        },
        'cap_exp_budget': {
            'cube': 'capital',
            'aggregate': 'asset_register_summary.sum',
            'cut': {
                'item.code': '4100',
                'amount_type.label': 'Adjusted Budget',
                'demarcation.code': str(geo_code),
            },
            'results': {}
        },
        'rep_maint': {
            'cube': 'repmaint',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '5005',
                'amount_type.label': 'Audited Actual',
                'demarcation.code': str(geo_code),
                'period_length.length': 'year'
            },
            'results': {}
        },
        'ppe': {
            'cube': 'bsheet',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '1300',
                'amount_type.label': 'Audited Actual',
                'demarcation.code': str(geo_code),
                'period_length.length': 'year',
            },
            'results': {}
        },
        'invest_prop': {
            'cube': 'bsheet',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '1401',
                'amount_type.label': 'Audited Actual',
                'demarcation.code': str(geo_code),
                'period_length.length': 'year',
            },
            'results': {}
        }
    }

    api_results = {}

    for item, details in line_items.iteritems():
        url = API_URL + api_query_string.format(
            cube=details['cube'],
            aggregate=details['aggregate'],
            cut='|'.join('{!s}:{!r}'.format(k, v) for (k, v) in details['cut'].iteritems()).replace("'", '"')
        )
        api_results[item] = requests.get(url, verify=False).json()
        for year in YEARS:
            details['results'][year] = amount_from_results(item, year, api_results, line_items)


    cash_coverage = {}
    op_budget_diff = {}
    cap_budget_diff = {}
    rep_maint_perc_ppe = {}

    for year in YEARS:
        cash_coverage[year] = ratio(
            line_items['cash_flow']['results'][year],
            (line_items['op_exp_actual']['results'][year] / 12),
            1)
        op_budget_diff[year] = percent(
            (line_items['op_exp_budget']['results'][year] - line_items['op_exp_actual']['results'][year]),
            line_items['op_exp_budget']['results'][year],
            1)
        cap_budget_diff[year] = percent(
            (line_items['cap_exp_budget']['results'][year] - line_items['cap_exp_actual']['results'][year]),
            line_items['cap_exp_budget']['results'][year])
        rep_maint_perc_ppe[year] = percent(line_items['rep_maint']['results'][year],
            (line_items['ppe']['results'][year] + line_items['invest_prop']['results'][year]))

    mayoral_staff = [
            {'label': 'Executive Mayor',
            'title': 'Mr',
            'name': 'Alfred Mtsi',
            'office_phone': '043 705 1072',
            'email': 'alfredm@buffalocity.gov.za',
            'secretary': {
                'title': 'Ms',
                'name': 'Yolisa Ntoni',
                'office_phone': '043 705 1072',
                'email': 'yolisan@buffalocity.gov.za'
            }
        },
        {
            'label': 'Deputy Executive Mayor',
            'title': 'Mr',
            'name': 'Xola Pakati',
            'office_phone': '043 705 2807',
            'email': 'philasandep@buffalocity.gov.za',
            'secretary': {
                'title': 'Ms',
                'name': 'Philasande Pula',
                'office_phone': '043 705 2899',
                'email': 'philasandep@buffalocity.gov.za',
            }
        },
        {
            'label': 'Chief financial officer',
            'title': 'Mr',
            'name': 'Vincent Pillay',
            'office_phone': '043 705 1892',
            'email': 'vincentp@buffalocity.gov.za',
            'secretary': {
                'title': 'Ms',
                'name': 'Candice Bahlmann',
                'office_phone': '043 705 1887',
                'email': 'candiceb@buffalocity.gov.za',
            }
        },
        {
            'label': 'Municipal Manager',
            'title': 'Mr',
            'name': 'Nceba Ncunyana',
            'office_phone': '043 705 1901',
            'email': 'ncebaAC@buffalocity.gov.za',
            'secretary': {
                'title': 'Ms',
                'name': 'Mandisa Mgoqi',
                'office_phone': '043 705 1901',
                'email': 'mandisamg@buffalocity.gov.za',
            }
        }
    ]

    return {
        'cash_coverage': cash_coverage,
        'op_budget_diff': op_budget_diff,
        'cap_budget_diff': cap_budget_diff,
        'rep_maint_perc_ppe': rep_maint_perc_ppe,
        'mayoral_staff': mayoral_staff}
