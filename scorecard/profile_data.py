from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from collections import defaultdict, OrderedDict
import dateutil.parser
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
    def __init__(self):
        self.API_URL = settings.API_URL + "/cubes/"
        self.session = FuturesSession(executor=EXECUTOR)

    def api_get(self, query):
        if query['query_type'] == 'aggregate':
            url = self.API_URL + query['cube'] + '/aggregate'
            params = {
                'aggregates': query['aggregate'],
                'cut': self.format_cut_param(query['cut']),
                'drilldown': '|'.join(query['drilldown']),
                'order': 'financial_year_end.year:desc',
                'page': 0,
            }
        elif query['query_type'] == 'facts':
            url = self.API_URL + query['cube'] + '/facts'
            params = {
                'cut': self.format_cut_param(query['cut']),
                'fields': ','.join(field for field in query['fields']),
                'page': 0
            }
        elif query['query_type'] == 'model':
            url = self.API_URL + query['cube'] + '/model'
            params = {}

        return self.session.get(url, params=params, verify=False)

    def format_cut_param(self, cuts):
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
    def __init__(self, geo_code, years=YEARS, client=None):
        self.years = list(years)
        self.geo_code = str(geo_code)
        self.budget_year = self.years[0] + 1
        self.client = client or MuniApiClient()

        self.revenue_breakdown_items = [
            ('Property rates', '0200'),
            ('Service charges', '0400'),
            ('Transfers received', '1600'),
            ('Own revenue', '1700'),
        ]

    def calculate(self):
        self.queries = self.get_queries()
        self.results = defaultdict(dict)

        # api_get returns a future, so fire off a bunch of
        # requests and then only start collecting them later
        responses = []
        for query_name, query in self.queries.iteritems():
            responses.append((query_name, query, self.client.api_get(query)))

        for (query_name, query, response) in responses:
            self.results[query_name] = self.response_to_results(response, query)

    def response_to_results(self, api_response, query):
        api_response.result().raise_for_status()
        response_dict = api_response.result().json()
        if query['query_type'] == 'facts':
            return query['results_structure'](query, response_dict['data'])
        elif query['query_type'] == 'aggregate':
            return query['results_structure'](query, response_dict['cells'])
        elif query['query_type'] == 'model':
            return query['results_structure'](query, response_dict['model'])

    def cash_coverage(self):
        values = []
        for year in self.years:
            try:
                cash = self.results['cash_flow']['4200'][year]
                monthly_expenses = self.results['op_exp_actual']['4600'][year] / 12
                result = max(ratio(cash, monthly_expenses, 1), 0)
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
                op_ex_budget = self.results['op_exp_budget']['4600'][year]
                op_ex_actual = self.results['op_exp_actual']['4600'][year]
                result = percent((op_ex_actual - op_ex_budget), op_ex_budget, 1)
                overunder = 'under' if result < 0 else 'over'
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
            values.append({
                'year': year,
                'result': abs(result) if result is not None else None,
                'overunder': overunder,
                'rating': rating
            })

        return values

    def cap_budget_diff(self):
        values = []
        for year in self.years:
            try:
                cap_ex_budget = self.results['cap_exp_budget']['4100'][year]
                cap_ex_actual = self.results['cap_exp_actual']['4100'][year]
                result = percent((cap_ex_actual - cap_ex_budget), cap_ex_budget)
                overunder = 'under' if result < 0 else 'over'
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
            values.append({
                'year': year,
                'result': abs(result) if result is not None else None,
                'overunder': overunder,
                'rating': rating
            })

        return values

    def rep_maint_perc_ppe(self):
        values = []
        for year in self.years:
            try:
                rep_maint = self.results['rep_maint']['5005'][year]
                ppe = self.results['ppe']['1300'][year]
                invest_prop = self.results['invest_prop']['1401'][year]
                result = percent(rep_maint, (ppe + invest_prop))
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
        for year in self.years + [self.budget_year]:
            year_name = year if year != self.budget_year else ("%s budget" % year)
            subtotal = 0.0
            try:
                total = self.results['revenue_breakdown']['1900'][year]

                for item, code in self.revenue_breakdown_items:
                    amount = self.results['revenue_breakdown'][code][year]
                    subtotal += amount
                    values.append({
                        'item': item,
                        'amount': amount,
                        'percent': percent(amount, total),
                        'year': year_name,
                    })
                if total and subtotal and (total != subtotal):
                    values.append({
                        'item': 'Other',
                        'amount': total - subtotal,
                        'percent': percent(total - subtotal, total),
                        'year': year_name,
                    })
            except KeyError:
                continue
        return values

    def expenditure_trends(self):
        values = defaultdict(list)
        for year in self.years:
            try:
                total = self.results['expenditure_breakdown']['4600'][year]
            except KeyError:
                total = None

            try:
                staff = percent(self.results['expenditure_breakdown']['3000'][year] +
                                self.results['expenditure_breakdown']['3100'][year],
                                total)
            except KeyError:
                staff = None

            try:
                contracting = percent(self.results['expenditure_breakdown']['4200'][year], total)
            except KeyError:
                contracting = None

            values['staff'].append({'year': year, 'result': staff})
            values['contracting'].append({'year': year, 'result': contracting})

        return values

    def expenditure_functional_breakdown(self):
        GAPD_categories = {
            'Budget & Treasury Office',
            'Executive & Council',
            'Planning and Development',
            'Corporate Services',
        }
        GAPD_label = 'Governance, Administration, Planning and Development'

        results = self.results['expenditure_functional_breakdown']
        grouped_results = []

        for year, yeargroup in groupby(results, lambda r: r['financial_year_end.year']):
            try:
                total = self.results['expenditure_breakdown']['4600'][year]
                GAPD_total = 0.0
                year_name = year if year != self.budget_year else ("%s budget" % year)

                for result in yeargroup:
                    # only do budget for budget year, use auda for others
                    if self.check_budget_actual(year, result['amount_type.code']):
                        if result['function.category_label'] in GAPD_categories:
                            GAPD_total += (result['amount.sum'] or 0)
                        else:
                            grouped_results.append({
                                'amount': result['amount.sum'] or 0,
                                'percent': percent((result['amount.sum'] or 0), total),
                                'item': result['function.category_label'],
                                'year': year_name,
                            })

                grouped_results.append({
                    'amount': GAPD_total,
                    'percent': percent(GAPD_total, total),
                    'item': GAPD_label,
                    'year': year_name,
                })
            except KeyError:
                continue

        return sorted(grouped_results, key=lambda r: (r['year'], r['item']))

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
                op_ex_actual = self.results['op_exp_actual']['4600'][year]
                result = percent(aggregate[year], op_ex_actual)
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
                if secretary['name'] is None:
                    secretary = None
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

    def check_budget_actual(self, year, amount_type):
        return (year == self.budget_year and amount_type == 'ORGB'
                or year != self.budget_year and amount_type != 'ORGB')

    def item_code_year_aggregate(self, query, response):
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

        # should we handle budget years differently?
        if query.get('split_on_budget'):
            response = [r for r in response
                        if self.check_budget_actual(r['financial_year_end.year'], r['amount_type.code'])]

        for code in query['cut']['item.code']:
            # Index values by financial period, treating nulls as zero
            results[code] = OrderedDict([
                (c['financial_year_end.year'], c[query['aggregate']] or 0)
                for c in response if c['item.code'] == code])
        return results

    def noop_structure(self, query, response):
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
                    'amount_type.code': ['AUDA', 'ORGB'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years + [self.budget_year],
                },
                'drilldown': YEAR_ITEM_DRILLDOWN + ['amount_type.code'],
                'query_type': 'aggregate',
                'results_structure': self.item_code_year_aggregate,
                'split_on_budget': True,
            },
            'expenditure_breakdown': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': [
                        '3000', '3100', '4200', '4600',
                    ],
                    'amount_type.code': ['AUDA', 'ORGB'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years + [self.budget_year],
                },
                'drilldown': YEAR_ITEM_DRILLDOWN + ['amount_type.code'],
                'query_type': 'aggregate',
                'results_structure': self.item_code_year_aggregate,
                'split_on_budget': True,
            },
            'expenditure_functional_breakdown': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['4600'],
                    'amount_type.code': ['AUDA', 'ORGB'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years + [self.budget_year]
                },
                'drilldown': [
                    'function.category_label',
                    'financial_year_end.year',
                    'amount_type.code',
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
