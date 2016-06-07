from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from collections import defaultdict, OrderedDict, Counter
import dateutil.parser
import copy


from django.conf import settings

from wazimap.data.utils import percent, ratio

EXECUTOR = ThreadPoolExecutor(max_workers=10)

# The years for which we need results. Must be in desceneding order.
YEARS = [2015, 2014, 2013, 2012]

YEAR_ITEM_DRILLDOWN = [
    'item.code',
    'item.label',
    'financial_year_end.year',
]


class MuniApiClient(object):
    def __init__(self, geo_code):
        self.API_URL = settings.API_URL + "/cubes/"
        self.geo_code = str(geo_code)
        self.years = YEARS
        self.current_year = YEARS[:1]

        self.line_item_params = self.get_line_item_params()
        self.results = defaultdict(dict)

        responses = []
        self.session = FuturesSession(executor=EXECUTOR)
        for line_item, query_params in self.line_item_params.iteritems():
            responses.append((line_item, query_params, self.api_get(query_params)))

        for (line_item, query_params, response) in responses:
            self.results[line_item] = \
                self.response_to_results(response, query_params)

    def api_get(self, query_params):
        if query_params['query_type'] == 'aggregate':
            url = self.API_URL + query_params['cube'] + '/aggregate'
            params = {
                'aggregates': query_params['aggregate'],
                'cut': '|'.join('{!s}:{!s}'.format(
                    k, ';'.join('{!r}'.format(item) for item in v))
                    for (k, v) in query_params['cut'].iteritems()
                    ).replace("'", '"'),
                'drilldown': '|'.join(query_params['drilldown']),
                'order': 'financial_year_end.year:desc',
                'page': 0,
            }
        elif query_params['query_type'] == 'facts':
            url = self.API_URL + query_params['cube'] + '/facts'
            params = {
                'cut': '|'.join('{!s}:{!r}'.format(k, v)
                    for (k, v) in query_params['cut'].iteritems()
                ).replace("'", '"'),
                'fields': ','.join(field for field in query_params['fields']),
                'page': 0
            }
        elif query_params['query_type'] == 'model':
            url = self.API_URL + query_params['cube'] + '/model'
            params = {}
        return self.session.get(url, params=params, verify=False)

    def response_to_results(self, api_response, query_params):
        api_response.result().raise_for_status()
        response_dict = api_response.result().json()
        if query_params['query_type'] == 'facts':
            results = self.facts_from_response(response_dict, query_params)
        elif query_params['query_type'] == 'aggregate':
            results = self.aggregate_from_response(response_dict, query_params)
        elif query_params['query_type'] == 'model':
            results = response_dict['model']

        return results

    @staticmethod
    def aggregate_from_response(response, query_params):
        """
        Results are the values we received from the API converted into the following format:
        {
            '4100': {2015: 11981070609.0}, {2014: 844194485.0}, {2013: 593485329.0}
        }
        """
        results = {}
        for code in query_params['cut']['item.code']:
          # Index values by financial period, treating nulls as zero
          results[code] = OrderedDict([
              (c['financial_year_end.year'], c[query_params['aggregate']] or 0)
              for c in response['cells'] if c['item.code'] == code])

        return results

    @staticmethod
    def facts_from_response(response, query_params):
        return response['data']

    def get_line_item_params(self):
        return {
            'op_exp_actual': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['4600'],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'op_exp_budget': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['4600'],
                    'amount_type.code': ['ADJB'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'cash_flow': {
                'cube': 'cflow',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['4200'],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'cap_exp_actual': {
                'cube': 'capital',
                'aggregate': 'asset_register_summary.sum',
                'cut': {
                    'item.code': ['4100'],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'cap_exp_budget': {
                'cube': 'capital',
                'aggregate': 'asset_register_summary.sum',
                'cut': {
                    'item.code': ['4100'],
                    'amount_type.code': ['ADJB'],
                    'demarcation.code': [self.geo_code],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'rep_maint': {
                'cube': 'repmaint',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['5005'],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'ppe': {
                'cube': 'bsheet',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['1300'],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'invest_prop': {
                'cube': 'bsheet',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['1401'],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'wasteful_exp': {
                'cube': 'badexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['irregular', 'fruitless', 'unauthorised'],
                    'demarcation.code': [self.geo_code],
                    'financial_year_end.year': self.years,
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'revenue_breakdown': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['0200', '0400', '1600', '1700', '1900'],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'expenditure_breakdown': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['3000', '3100', '3400', '4100', '4200', '4300', '3700', '4600'],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'expenditure_trends': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['3000', '3100', '4200', '4600', ],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
            },
            'officials': {
                'cube': 'officials',
                'cut': {
                    'municipality.demarcation_code': self.geo_code,
                },
                'fields': [
                    'role.role',
                    'contact_details.title',
                    'contact_details.name',
                    'contact_details.email_address',
                    'contact_details.phone_number',
                    'contact_details.fax_number'],
                'value_label': '',
                'query_type': 'facts',
            },
            'officials_date': {
                'cube': 'officials',
                'query_type': 'model',
            },
            'contact_details' : {
                'cube': 'municipalities',
                'cut': {
                    'municipality.demarcation_code': self.geo_code,
                },
                'fields': [
                    'municipality.phone_number',
                    'municipality.street_address_1',
                    'municipality.street_address_2',
                    'municipality.street_address_3',
                    'municipality.street_address_4',
                    'municipality.url'
                ],
                'value_label': '',
                'query_type': 'facts',
            },
            'audit_opinions' : {
                'cube': 'audit_opinions',
                'cut': {
                    'demarcation.code': self.geo_code
                },
                'fields': [
                    'opinion.code',
                    'opinion.label',
                    'opinion.report_url',
                    'financial_year_end.year'
                ],
                'value_label': 'opinion.label',
                'query_type': 'facts',
            },
        }


class IndicatorCalculator(object):
    def __init__(self, results, years):
        self.results = results
        self.years = years
        self.current_year = YEARS[0]

        self.revenue_breakdown_items = [
            ('Property rates', '0200'),
            ('Service charges', '0400'),
            ('Transfers received', '1600'),
            ('Own revenue', '1700'),
            ('Total', '1900')
        ]

        self.expenditure_breakdown_items = [
            ('Employee related costs', ['3000', '3100']),
            ('Councillor remuneration', '3400'),
            ('Bulk purchases', '4100'),
            ('Contracted services', '4200'),
            ('Transfers spent', '4300'),
            ('Depreciation and amortisation', '3700'),
            ('Total', '4600')
        ]

    def cash_coverage(self):
        values = []
        for year in self.years:
            try:
                result = ratio(
                    self.results['cash_flow']['4200'][year],
                    (self.results['op_exp_actual']['4600'][year] / 12),
                    1)
                if result > 3:
                    rating = 'good'
                elif result <= 1:
                    rating = 'bad'
                else:
                    rating = 'ave'
            except KeyError:
                result = None
                rating = None
            values.append({'year': year, 'result': result, 'rating': rating})

        return values

    def op_budget_diff(self):
        values = []
        for year in self.years:
            try:
                result = percent(
                    (self.results['op_exp_budget']['4600'][year] - self.results['op_exp_actual']['4600'][year]),
                    self.results['op_exp_budget']['4600'][year],
                    1)
                if abs(result) < 10:
                    rating = 'good'
                elif abs(result) <= 25:
                    rating = 'ave'
                elif abs(result) > 25:
                    rating = 'bad'
                else:
                    rating = None
            except KeyError:
                result = None
                rating = None
            values.append({'year': year, 'result': result, 'rating': rating})

        return values

    def cap_budget_diff(self):
        values = []
        for year in self.years:
            try:
                result = percent(
                    (self.results['cap_exp_budget']['4100'][year] - self.results['cap_exp_actual']['4100'][year]),
                    self.results['cap_exp_budget']['4100'][year])
                if abs(result) < 10:
                    rating = 'good'
                elif abs(result) <= 30:
                    rating = 'ave'
                elif abs(result) > 30:
                    rating = 'bad'
                else:
                    rating = None
            except KeyError:
                result = None
                rating = None
            values.append({'year': year, 'result': result, 'rating': rating})

        return values

    def rep_maint_perc_ppe(self):
        values = []
        for year in self.years:
            try:
                result = percent(self.results['rep_maint']['5005'][year],
                (self.results['ppe']['1300'][year] + self.results['invest_prop']['1401'][year]))
                if abs(result) >= 8:
                    rating = 'good'
                elif abs(result) < 8:
                    rating = 'bad'
                else:
                    rating = None
            except KeyError:
                result = None
                rating = None

            values.append({'year': year, 'result': result, 'rating': rating})

        return values

    def revenue_breakdown(self):
        values = []
        for year in self.years:
            subtotal = 0.0
            for item, code in self.revenue_breakdown_items:
                try:
                    amount = self.results['revenue_breakdown'][code][year]
                    if not item == 'Total':
                        subtotal += amount
                    else:
                        total = amount
                except KeyError:
                    amount = None
                if not item == 'Total':
                    values.append({'item': item, 'amount': amount, 'year': year})
            if total and subtotal:
                values.append({'item': 'Other', 'amount': total - subtotal, 'year': year})
        return values

    def expenditure_trends(self):
        values = []

        for year in self.years:
            try:
                staff = self.results['expenditure_breakdown']['3000'][year] \
                        + self.results['expenditure_breakdown']['3100'][year]
                contracting = self.results['expenditure_breakdown']['4200'][year]
                total = self.results['expenditure_breakdown']['4600'][year]
                values.append({
                    'contracting': (contracting/total)*100,
                    'staff': (staff/total)*100,
                    'year': year,
                })
            except KeyError:
                values.append({
                    'contracting': None,
                    'staff': None,
                    'year': year,
                })

        return values

    def expenditure_breakdown(self):
        values = []

        for year in self.years:
            subtotal = 0.0
            for item, code in self.expenditure_breakdown_items:
                try:
                    if not type(code) is list:
                        amount = self.results['expenditure_breakdown'][code][year]
                    else:
                        amount = 0.0
                        for c in code:
                            amount += self.results['expenditure_breakdown'][c][year]
                    if not item == 'Total':
                        subtotal += amount
                    else:
                        total = amount
                except KeyError:
                    amount = None
                if not item == 'Total':
                    values.append({'item': item, 'amount': amount, 'year': year})

            if total and subtotal:
                values.append({'item': 'Other', 'amount': total - subtotal, 'year': year})
        return values

    def cash_at_year_end(self):
        values = []
        for year, result in self.results['cash_flow']['4200'].iteritems():
            if result > 0:
                rating = 'good'
            elif result <= 0:
                rating = 'bad'
            else:
                rating = None

            values.append({'year': year, 'result': result, 'rating': rating})

        return values

    def wasteful_exp_perc_exp(self):
        values = []
        aggregate = {}
        for item, results in self.results['wasteful_exp'].iteritems():
            for year, amount in results.iteritems():
                if year in aggregate:
                    aggregate[year] += amount
                else:
                    aggregate[year] = amount

        for year in self.years:
            try:
                result = percent(aggregate[year],
                    self.results['op_exp_actual']['4600'][year])
                rating = None
                if result == 0:
                    rating = 'good'
                else:
                    rating = 'bad'
            except KeyError:
                result = None
                rating = None

            values.append({'year': year, 'result': result, 'rating': rating})
        return values

    def mayoral_staff(self):
        roles = [
            'Mayor/Executive Mayor',
            'Municipal Manager',
            'Deputy Mayor/Executive Mayor',
            'Chief Financial Officer',
        ]

        secretaries = {
            'Mayor/Executive Mayor': 'Secretary of Mayor/Executive Mayor',
            'Municipal Manager': 'Secretary of Municipal Manager',
            'Deputy Mayor/Executive Mayor': 'Secretary of Deputy Mayor/Executive Mayor',
            'Chief Financial Officer': 'Secretary of Financial Manager',
        }

        # index officials by role
        officials = {
            f['role.role']: {
                'role': f['role.role'],
                'title': f['contact_details.title'],
                'name': f['contact_details.name'],
                'office_phone': f['contact_details.phone_number'],
                'fax_number': f['contact_details.fax_number'],
                'email': f['contact_details.email_address']
            } for f in self.results['officials']
        }

        # fold in secretaries
        for role in roles:
            official = officials.get(role)
            if official:
                secretary = officials.get(secretaries[role])
                if secretary:
                    official['secretary'] = secretary

        date = self.results['officials_date'].get('last_updated')
        if date:
            date = dateutil.parser.parse(date).strftime("%B %Y")

        return {
            'officials': [officials.get(role) for role in roles],
            'updated_date': date,
        }

    def muni_contact(self):
        muni_contact = self.results['contact_details'][0]
        values = {
            'street_address_1': muni_contact['municipality.street_address_1'],
            'street_address_2': muni_contact['municipality.street_address_2'],
            'street_address_3': muni_contact['municipality.street_address_3'],
            'street_address_4': muni_contact['municipality.street_address_4'],
            'phone_number': muni_contact['municipality.phone_number'],
            'url': muni_contact['municipality.url']
        }

        return values

    def audit_opinions(self):
        values = []
        for result in self.results['audit_opinions']:
            values.append({
                'year': result['financial_year_end.year'],
                'result': result['opinion.label'],
                'rating': result['opinion.code'],
                'report_url': result['opinion.report_url'],
            })
        values = sorted(values, key=lambda r: r['year'])
        values.reverse()
        return values
