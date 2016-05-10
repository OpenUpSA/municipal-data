import requests
from collections import defaultdict
import json

from wazimap.data.utils import percent, ratio

API_URL = 'https://data.municipalmoney.org.za/api/cubes/'
YEARS = [2015, 2014, 2013, 2012, 2011]

def aggregate_from_response(item, year, response, line_items):
    """
    Returns the aggregated values we received from the API for the specified year.
    If the 'cells' list in the results is empty, no values were returned,
    and for now, we return zero in that case.
    We should be returning None, and checking for None values in the ratio calculation.
    """
    for cell in response[item]['cells']:
        if cell['financial_period.period'] == year:
            return cell[line_items[item]['aggregate']]
    return 0

def annual_facts_from_response(item, response, line_items):
    value_label = line_items[item]['value_label']
    return {i['financial_year_end.year']: i[value_label] for i in response[item]['data']}

def facts_from_response(item, response, line_items):
    return response[item]['data']

def get_profile(geo_code, geo_level, profile_name=None):

    api_query_strings = {
        'aggregate': '{cube}/aggregate?aggregates={aggregate}&cut={cut}&drilldown=item.code|item.label|financial_period.period&page=0',
        'facts': '{cube}/facts?&cut={cut}&drilldown=item.code|item.label|financial_period.period&page=0',
    }

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
            'query_type': 'aggregate',
        },
        'op_exp_budget': {
            'cube': 'incexp',
            'aggregate': 'amount.sum',
            'cut': {
                'item.code': '4600',
                'amount_type.label': 'Adjusted Budget',
                'demarcation.code': str(geo_code),
            },
            'query_type': 'aggregate',
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
            'query_type': 'aggregate',
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
            'query_type': 'aggregate',
        },
        'cap_exp_budget': {
            'cube': 'capital',
            'aggregate': 'asset_register_summary.sum',
            'cut': {
                'item.code': '4100',
                'amount_type.label': 'Adjusted Budget',
                'demarcation.code': str(geo_code),
            },
            'query_type': 'aggregate',
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
            'query_type': 'aggregate',
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
            'query_type': 'aggregate',
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
            'query_type': 'aggregate',
        },
        'officials': {
            'cube': 'officials',
            'facts': '',
            'cut': {
                'municipality.demarcation_code': str(geo_code),
            },
            'query_type': 'facts',
            'annual': False,
            'value_label': ''
        },
        'contact_details' : {
            'cube': 'municipalities',
            'facts': '',
            'cut': {
                'municipality.demarcation_code': str(geo_code),
            },
            'query_type': 'facts',
            'annual': False,
            'value_label': ''
        },
        'audit_opinions' : {
            'cube': 'audit_opinions',
            'facts': '',
            'cut': {
                'municipality.demarcation_code': str(geo_code),
            },
            'query_type': 'facts',
            'annual': True,
            'value_label': 'opinion.label'
        }
    }

    api_response = {}
    results = defaultdict(dict)
    for item, params in line_items.iteritems():
        if params['query_type'] == 'aggregate':
            url = API_URL + api_query_strings['aggregate'].format(
                aggregate=params['aggregate'],
                cube=params['cube'],
                cut='|'.join('{!s}:{!r}'.format(k, v) for (k, v) in params['cut'].iteritems()).replace("'", '"')
            )
        elif params['query_type'] == 'facts':
            url = API_URL + api_query_strings['facts'].format(
                facts=params['facts'],
                cube=params['cube'],
                cut='|'.join('{!s}:{!r}'.format(k, v) for (k, v) in params['cut'].iteritems()).replace("'", '"')
            )

        api_response[item] = requests.get(url, verify=False).json()
        if params['query_type'] == 'facts':
            if params['annual']:
                results[item] = annual_facts_from_response(item, api_response, line_items)
            else:
                results[item] = facts_from_response(item, api_response, line_items)
        else:
            for year in YEARS:
                results[item][year] = aggregate_from_response(item, year, api_response, line_items)

    cash_coverage = {}
    op_budget_diff = {}
    cap_budget_diff = {}
    rep_maint_perc_ppe = {}

    for year in YEARS:
        cash_coverage[year] = ratio(
            results['cash_flow'][year],
            (results['op_exp_actual'][year] / 12),
            1)
        op_budget_diff[year] = percent(
            (results['op_exp_budget'][year] - results['op_exp_actual'][year]),
            results['op_exp_budget'][year],
            1)
        cap_budget_diff[year] = percent(
            (results['cap_exp_budget'][year] - results['cap_exp_actual'][year]),
            results['cap_exp_budget'][year])
        rep_maint_perc_ppe[year] = percent(results['rep_maint'][year],
            (results['ppe'][year] + results['invest_prop'][year]))


    mayoral_staff = []
    exclude_roles = ['Speaker',  'Secretary of Speaker']

    for official in results['officials']:
        if not official['role.role'] in exclude_roles:
            mayoral_staff.append({
                'role': official['role.role'],
                'title': official['contact_details.title'],
                'name': official['contact_details.name'],
                'office_phone': official['contact_details.phone_number'],
                'fax_number': official['contact_details.fax_number'],
                'email': official['contact_details.email_address']
            })

    muni_contact = results['contact_details'][0]
    contact_details = {
        'street_address_1': muni_contact['municipality.street_address_1'],
        'street_address_2': muni_contact['municipality.street_address_2'],
        'street_address_3': muni_contact['municipality.street_address_3'],
        'street_address_4': muni_contact['municipality.street_address_4'],
        'postal_address_1': muni_contact['municipality.postal_address_1'],
        'postal_address_2': muni_contact['municipality.postal_address_2'],
        'postal_address_3': muni_contact['municipality.postal_address_3'],
        'phone_number': muni_contact['municipality.phone_number'],
        'url': muni_contact['municipality.url'].lower()
    }

    audit_opinions = results['audit_opinions']

    return {
        'cash_coverage': cash_coverage,
        'op_budget_diff': op_budget_diff,
        'cap_budget_diff': cap_budget_diff,
        'rep_maint_perc_ppe': rep_maint_perc_ppe,
        'mayoral_staff': mayoral_staff,
        'contact_details': contact_details,
        'audit_opinions': audit_opinions}
