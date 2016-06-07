from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from collections import defaultdict, OrderedDict
import dateutil.parser
import copy
from itertools import groupby


from django.conf import settings

from wazimap.data.utils import percent, ratio

EXECUTOR = ThreadPoolExecutor(max_workers=10)

# The years for which we need results. Must be in desceneding order.
YEARS = [2015, 2014, 2013, 2012]

YEAR_ITEM_DRILLDOWN = [
    'item.code',
    'financial_year_end.year',
]


class MuniApiClient(object):
    def __init__(self, geo_code):
        self.API_URL = settings.API_URL + "/cubes/"
        self.geo_code = str(geo_code)
        self.years = YEARS
        self.current_year = YEARS[:1]

        self.queries = self.get_queries()
        self.results = defaultdict(dict)

        responses = []
        self.session = FuturesSession(executor=EXECUTOR)
        for query_name, query in self.queries.iteritems():
            responses.append((query_name, query, self.api_get(query)))

        for (query_name, query, response) in responses:
            self.results[query_name] = \
                self.response_to_results(response, query)

    def api_get(self, query):
        if query['query_type'] == 'aggregate':
            url = self.API_URL + query['cube'] + '/aggregate'
            params = {
                'aggregates': query['aggregate'],
                'cut': format_cut_param(query['cut']),
                'drilldown': '|'.join(query['drilldown']),
                'order': 'financial_year_end.year:desc',
                'page': 0,
            }
        elif query['query_type'] == 'facts':
            url = self.API_URL + query['cube'] + '/facts'
            params = {
                'cut': format_cut_param(query['cut']),
                'fields': ','.join(field for field in query['fields']),
                'page': 0
            }
        elif query['query_type'] == 'model':
            url = self.API_URL + query['cube'] + '/model'
            params = {}
        return self.session.get(url, params=params, verify=False)

    def response_to_results(self, api_response, query):
        api_response.result().raise_for_status()
        response_dict = api_response.result().json()
        if query['query_type'] == 'facts':
            return query['results_structure'](query, response_dict['data'])
        elif query['query_type'] == 'aggregate':
            return query['results_structure'](query, response_dict['cells'])
        elif query['query_type'] == 'model':
            return query['results_structure'](query, response_dict['model'])

    @staticmethod
    def item_code_year_aggregate(query, response):
        """
        Results are the values we received from the API converted into the
        following format:
        {
            '4100': [
                {2015: 11981070609.0},
                {2014: 844194485.0},
                {2013: 593485329.0}
            ]
        }
        """
        results = {}
        for code in query['cut']['item.code']:
            # Index values by financial period, treating nulls as zero
            results[code] = OrderedDict([
              (c['financial_year_end.year'], c[query['aggregate']] or 0)
              for c in response if c['item.code'] == code])
        return results

    @staticmethod
    def noop_structure(query, response):
        return response

    def get_queries(self):
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
                'results_structure': self.item_code_year_aggregate,
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
                'results_structure': self.item_code_year_aggregate,
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
                'results_structure': self.item_code_year_aggregate,
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
                'results_structure': self.item_code_year_aggregate,
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
                'results_structure': self.item_code_year_aggregate,
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
                'results_structure': self.item_code_year_aggregate,
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
                'results_structure': self.item_code_year_aggregate,
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
                'results_structure': self.item_code_year_aggregate,
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
                'results_structure': self.item_code_year_aggregate,
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
                'results_structure': self.item_code_year_aggregate,
            },
            'expenditure_breakdown': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': [
                        '3000', '3100', '4200', '4600',
                    ],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
                'results_structure': self.item_code_year_aggregate,
            },
            'expenditure_functional_breakdown': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['4600'],
                    'amount_type.code': ['AUDA'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years[:2]
                },
                'drilldown': [
                    'function.category_label',
                    'financial_year_end.year',
                ],
                'query_type': 'aggregate',
                'results_structure': self.noop_structure,
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
                'results_structure': self.item_code_year_aggregate,
            },
            'officials': {
                'cube': 'officials',
                'cut': {
                    'municipality.demarcation_code': [self.geo_code],
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
                'results_structure': self.noop_structure,
            },
            'officials_date': {
                'cube': 'officials',
                'query_type': 'model',
                'results_structure': self.noop_structure,
            },
            'contact_details': {
                'cube': 'municipalities',
                'cut': {
                    'municipality.demarcation_code': [self.geo_code],
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
                'results_structure': self.noop_structure,
            },
            'audit_opinions': {
                'cube': 'audit_opinions',
                'cut': {
                    'demarcation.code': [self.geo_code],
                    'financial_year_end.year': self.years[:4],
                },
                'fields': [
                    'opinion.code',
                    'opinion.label',
                    'opinion.report_url',
                    'financial_year_end.year'
                ],
                'value_label': 'opinion.label',
                'query_type': 'facts',
                'results_structure': self.noop_structure,
            },
        }


def format_cut_param(cuts):
    keypairs = []
    for key, vals in cuts.iteritems():
        vals_as_strings = []
        for val in vals:
            if type(val) == str:
                vals_as_strings.append('"' + val + '"')
            if type(val) == int:
                vals_as_strings.append(str(val))
        keypairs.append((key, ';'.join(vals_as_strings)))
    return '|'.join('{!s}:{!s}'.format(pair[0], pair[1]) for pair in keypairs)


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
                    (self.results['op_exp_budget']['4600'][year]
                     - self.results['op_exp_actual']['4600'][year]),
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
                    (self.results['cap_exp_budget']['4100'][year]
                     - self.results['cap_exp_actual']['4100'][year]),
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
                                 (self.results['ppe']['1300'][year]
                                  + self.results['invest_prop']['1401'][year]))
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

    def expenditure_functional_breakdown(self):
        GAPD_categories = {
            'Budget & Treasury Office',
            'Executive & Council',
            'Planning and Development',
        }
        GAPD_label = 'Governance, Administration, Planning and Development'
        results = self.results['expenditure_functional_breakdown']
        keyfun = lambda r: r['financial_year_end.year']
        grouped_results = []
        years = sorted(list(set(r['financial_year_end.year'] for r in results)))
        years.reverse()
        for year, yeargroup in groupby(results, keyfun):
            if year in years:
                total = self.results['expenditure_breakdown']['4600'][year]
                GAPD_total = 0.0
                for result in yeargroup:
                    if result['function.category_label'] in GAPD_categories:
                        GAPD_total += result['amount.sum']
                    else:
                        grouped_results.append({
                            'amount': (result['amount.sum']/total)*100,
                            'item': result['function.category_label'],
                            'year': result['financial_year_end.year'],
                        })
                grouped_results.append({
                    'amount': (GAPD_total/total)*100,
                    'item': GAPD_label,
                    'year': year
                })
        return sorted(grouped_results, key=lambda r: str(r['year'])+r['item'])

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
