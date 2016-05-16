import requests
from collections import defaultdict, OrderedDict

from wazimap.data.utils import percent, ratio
from wazimap.data.tables import get_datatable

API_URL = 'https://data.municipalmoney.org.za/api/cubes/'


def aggregate_from_response(item, response, line_items, years):
    """
    Return the aggregated values we received from the API by year,
    and build up the year set to determine which periods we
    use when presenting results.
    """
    results = OrderedDict([
        (c['financial_period.period'], c[line_items[item]['aggregate']])
        for c in response[item]['cells']])
    years |= set([year for year in results.keys()])

    return results, years


def annual_facts_from_response(item, response, line_items, years):
    """
    Return facts which change annually,
    and build up the year set to determine which periods we
    use when presenting results.
    """
    facts = OrderedDict([
        (i['financial_year_end.year'], i[line_items[item]['value_label']])
        for i in response[item]['data']])
    # Converting to int will not be needed once API returns all years as numbers
    years |= set([int(year) for year in facts.keys()])

    return facts, years

def facts_from_response(item, response, line_items):
    return response[item]['data']

def get_profile(geo_code, geo_level, profile_name=None):

    api_query_strings = {
        'aggregate': '{cube}/aggregate?aggregates={aggregate}&cut={cut}&drilldown=item.code|item.label|financial_period.period&page=0&order=financial_period.period:desc',
        'facts': '{cube}/facts?&cut={cut}&fields={fields}&page=0',
    }

    # Census data
    table = get_datatable('population')
    _, total_pop = table.get_stat_data(geo_level, geo_code, percent=False)

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
            'query_type': 'facts',
            'cube': 'officials',
            'cut': {
                'municipality.demarcation_code': str(geo_code),
            },
            'fields': [
                'role.role',
                'contact_details.title',
                'contact_details.name',
                'contact_details.email_address',
                'contact_details.phone_number',
                'contact_details.fax_number'],
            'annual': False,
            'value_label': ''
        },
        'contact_details' : {
            'query_type': 'facts',
            'cube': 'municipalities',
            'cut': {
                'municipality.demarcation_code': str(geo_code),
            },
            'fields': [
                'municipality.phone_number',
                'municipality.street_address_1',
                'municipality.street_address_2',
                'municipality.street_address_3',
                'municipality.street_address_4',
                'municipality.url'
            ],
            'annual': False,
            'value_label': ''
        },
        'audit_opinions' : {
            'query_type': 'facts',
            'cube': 'audit_opinions',
            'cut': {
                'municipality.demarcation_code': str(geo_code),
            },
            'fields': [
                'opinion.code',
                'opinion.label',
                'financial_year_end.year'
            ],
            'annual': True,
            'value_label': 'opinion.label'
        }
    }

    api_response = {}
    results = defaultdict(dict)
    years = set()

    for item, params in line_items.iteritems():
        if params['query_type'] == 'aggregate':
            url = API_URL + api_query_strings['aggregate'].format(
                aggregate=params['aggregate'],
                cube=params['cube'],
                cut='|'.join('{!s}:{!r}'.format(k, v) for (k, v) in params['cut'].iteritems()).replace("'", '"')
            )
        elif params['query_type'] == 'facts':
            url = API_URL + api_query_strings['facts'].format(
                cube=params['cube'],
                cut='|'.join('{!s}:{!r}'.format(k, v) for (k, v) in params['cut'].iteritems()).replace("'", '"'),
                fields=','.join(field for field in params['fields'])
            )

        api_response[item] = requests.get(url, verify=False).json()
        if params['query_type'] == 'facts':
            if params['annual']:
                results[item], years = annual_facts_from_response(item, api_response, line_items, years)
            else:
                results[item] = facts_from_response(item, api_response, line_items)
        else:
            results[item], years = aggregate_from_response(item, api_response, line_items, years)

    cash_coverage = OrderedDict()
    op_budget_diff = OrderedDict()
    cap_budget_diff = OrderedDict()
    rep_maint_perc_ppe = OrderedDict()

    for year in sorted(list(years), reverse=True):
        try:
            cash_coverage[year] = ratio(
                results['cash_flow'][year],
                (results['op_exp_actual'][year] / 12),
                1)
        except KeyError:
            cash_coverage[year] = None

        try:
            op_budget_diff[year] = percent(
                (results['op_exp_budget'][year] - results['op_exp_actual'][year]),
                results['op_exp_budget'][year],
                1)
        except KeyError:
            op_budget_diff[year] = None

        try:
            cap_budget_diff[year] = percent(
                (results['cap_exp_budget'][year] - results['cap_exp_actual'][year]),
                results['cap_exp_budget'][year])
        except KeyError:
            cap_budget_diff[year] = None

        try:
            rep_maint_perc_ppe[year] = percent(results['rep_maint'][year],
                (results['ppe'][year] + results['invest_prop'][year]))
        except KeyError:
            rep_maint_perc_ppe[year] = None

    cash_at_year_end = OrderedDict([
        (k, v) for k, v in results['cash_flow'].iteritems()
    ])

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
        'phone_number': muni_contact['municipality.phone_number'],
        'url': muni_contact['municipality.url'].lower()
    }

    audit_opinions = OrderedDict(sorted(results['audit_opinions'].items(), key=lambda t: t[0], reverse=True))

    return {
        'total_population': total_pop,
        'cash_coverage': cash_coverage,
        'op_budget_diff': op_budget_diff,
        'cap_budget_diff': cap_budget_diff,
        'rep_maint_perc_ppe': rep_maint_perc_ppe,
        'mayoral_staff': mayoral_staff,
        'contact_details': contact_details,
        'audit_opinions': audit_opinions,
        'cash_at_year_end': cash_at_year_end}
