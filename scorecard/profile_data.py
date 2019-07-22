"""
Municipality Profile data preparation
-------------------------------------
Gather data from the municipal finance API and provide values ready for display
on the page with little further processing.

If the API returns a null value, it can generally be treated as zero. That
happens in this library and nulls that should be zeros should not be
left to the frontend to handle.

The shape of data produced by this library is generally a series of years
or quarters in reverse chronological order with associated values. Only the
years that are to be shown are returned.

If data needed to calculate a value for a given date is missing, an
object is returned for that year with the value being None,
to indicate in the page that it is missing.
"""

from collections import defaultdict, OrderedDict
from concurrent.futures import ThreadPoolExecutor
from itertools import groupby
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from requests.packages.urllib3.util.retry import Retry
import dateutil.parser
import logging
import urllib

from .utils import percent, ratio

logger = logging.getLogger('municipal_finance')

EXECUTOR = ThreadPoolExecutor(max_workers=10)

# The years for which we need results. Must be in desceneding order.
LAST_AUDIT_YEAR = 2018
LAST_AUDIT_QUARTER = '2018q4'
YEARS = list(range(LAST_AUDIT_YEAR-3, LAST_AUDIT_YEAR+1))
YEARS.reverse()

LAST_OPINION_YEAR = 2018
AUDIT_OPINION_YEARS = list(range(LAST_OPINION_YEAR-3, LAST_OPINION_YEAR+1))
AUDIT_OPINION_YEARS.reverse()

# we'll actually only have data up to the year before this but use four
# for consistency on the page.
LAST_UIFW_YEAR = 2017
UIFW_YEARS = list(range(LAST_UIFW_YEAR-3, LAST_UIFW_YEAR+1))
UIFW_YEARS.reverse()

LAST_IN_YEAR_YEAR = 2018
IN_YEAR_YEARS = [LAST_IN_YEAR_YEAR+1, LAST_IN_YEAR_YEAR, LAST_IN_YEAR_YEAR-1, LAST_IN_YEAR_YEAR-2]


YEAR_ITEM_DRILLDOWN = [
    'item.code',
    'financial_year_end.year',
]


class APIOverloadedException(BaseException):
    pass


class MuniApiClient(object):
    def __init__(self, api_url):
        self.API_URL = api_url + "/cubes/"
        self.session = FuturesSession(executor=EXECUTOR)
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def api_get(self, query):
        if query['query_type'] == 'aggregate':
            url = self.API_URL + query['cube'] + '/aggregate'
            params = {
                'aggregates': query['aggregate'],
                'cut': self.format_cut_param(query['cut']),
                'drilldown': '|'.join(query['drilldown']),
                'page': 0,
            }
            if query.get('order'):
                params['order'] = query.get('order')
            else:
                params['order'] = 'financial_year_end.year:desc,item.code:asc'
        elif query['query_type'] == 'facts':
            url = self.API_URL + query['cube'] + '/facts'
            params = {
                'fields': ','.join(field for field in query['fields']),
                'page': 0
            }
            if query.get('cut'):
                params['cut'] = self.format_cut_param(query.get('cut'))
            if query.get('order'):
                params['order'] = query.get('order')

        elif query['query_type'] == 'model':
            url = self.API_URL + query['cube'] + '/model'
            params = {}

        params['pagesize'] = 20000

        logger.debug("API query %s?%s" % (url, urllib.parse.urlencode(params)))
        return self.session.get(url, params=params, verify=False)

    def format_cut_param(self, cuts):
        keypairs = []
        for key, vals in cuts.items():
            vals_as_strings = []
            for val in vals:
                if type(val) == str:
                    vals_as_strings.append('"' + val + '"')
                if type(val) == int:
                    vals_as_strings.append(str(val))
            keypairs.append((key, ';'.join(vals_as_strings)))
        return '|'.join('{!s}:{!s}'.format(pair[0], pair[1]) for pair in keypairs)


class APIData(object):
    def __init__(self, api_url, geo_code, years=YEARS, client=None):
        self.years = list(years)
        self.uifw_years = list(UIFW_YEARS)
        self.geo_code = str(geo_code)
        self.budget_year = self.years[0] + 1
        self.client = client or MuniApiClient(api_url)

        self.references = {
            'solgf': {
                'title': 'State of Local Government Finances',
                'url': 'http://mfma.treasury.gov.za/Media_Releases/The%20state%20of%20local%20government%20finances/Pages/default.aspx',
            },
            'circular71': {
                'title': 'Circular 71',
                'url': 'http://mfma.treasury.gov.za/Circulars/Pages/Circular71.aspx',
            },
            'overunder': {
                'title': 'Over and under spending reports to parliament',
                'url': 'http://mfma.treasury.gov.za/Media_Releases/Reports%20to%20Parliament/Pages/default.aspx',
            },
            'lges': {
                'title': 'Local Government Equitable Share',
                'url': 'http://mfma.treasury.gov.za/Media_Releases/LGESDiscussions/Pages/default.aspx',
            },
            'mbrr': {
                'title': 'Municipal Budget and Reporting Regulations',
                'url': 'http://mfma.treasury.gov.za/RegulationsandGazettes/Municipal%20Budget%20and%20Reporting%20Regulations/Pages/default.aspx',
            }
        }

    def fetch_data(self):
        self.queries = self.get_queries()
        self.results = defaultdict(dict)

        # api_get returns a future, so fire off a bunch of
        # requests and then only start collecting them later
        responses = []
        for query_name, query in self.queries.items():
            responses.append((query_name, query, self.client.api_get(query)))

        for (query_name, query, response) in responses:
            self.results[query_name] = self.response_to_results(response, query)

    def response_to_results(self, api_response, query):
        self.raise_if_overloaded(api_response.result())
        self.raise_if_paged(api_response.result())
        api_response.result().raise_for_status()
        response_dict = api_response.result().json()
        if query['query_type'] == 'facts':
            return query['results_structure'](query, response_dict['data'])
        elif query['query_type'] == 'aggregate':
            return query['results_structure'](query, response_dict['cells'])
        elif query['query_type'] == 'model':
            return query['results_structure'](query, response_dict['model'])

    def raise_if_overloaded(self, response):
        DB_TIMEOUT_MSG = "(psycopg2.extensions.QueryCanceledError) canceling statement due to statement timeout\n"
        if response.status_code == 500:
            if response.json().get("message") == DB_TIMEOUT_MSG:
                raise APIOverloadedException("API Overloaded")

    def raise_if_paged(self, response):
        body = response.json()
        if body.get("total_cell_count") == body.get("page_size") \
           and body.get("total_cell_count") is not None:
            url = response.url
            raise Exception("Page is full: should check next page for %s " % url)

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
                'date': result['financial_year_end.year'],
                'result': result['opinion.label'],
                'rating': result['opinion.code'],
                'report_url': result['opinion.report_url'],
            })
        values = sorted(values, key=lambda r: r['date'])
        values.reverse()
        return {'values': values}

    def check_budget_actual(self, year, amount_type):
        return (year == self.budget_year and amount_type == 'ORGB'
                or year != self.budget_year and amount_type != 'ORGB')

    def item_code_year_aggregate(self, query, response):
        """
        Restructure and ensure API nulls become zeros
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
                (c['financial_year_end.year'], c[query['aggregate']] or 0.0)
                for c in response if c['item.code'] == code])
        return results

    def noop_structure(self, query, response):
        """
        No restructuring, just ensure API nulls become zeros
        """
        if query['query_type'] == 'aggregate':
            aggregate = query['aggregate']
            for cell in response:
                cell[aggregate] = cell[aggregate] or 0.0
        return response

    def get_queries(self):
        return {
            # monthly values for in-year calculations from bsheet
            'in_year_bsheet': {
                'cube': 'bsheet',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['2150', '1600', '1800', '2200'],
                    'amount_type.code': ['ACT'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['month'],
                    'financial_year_end.year': IN_YEAR_YEARS,
                },
                'drilldown': YEAR_ITEM_DRILLDOWN + ['financial_period.period'],
                'query_type': 'aggregate',
                'results_structure': self.noop_structure,
            },
            'in_year_cflow': {
                'cube': 'cflow',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': [
                        '3010',
                        '3030',
                        '3040',
                        '3050',
                        '3060',
                        '3070',
                        '3100',
                    ],
                    'amount_type.code': ['ACT'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['month'],
                    'financial_year_end.year': IN_YEAR_YEARS,
                },
                'drilldown': YEAR_ITEM_DRILLDOWN + ['financial_period.period'],
                'query_type': 'aggregate',
                'results_structure': self.noop_structure,
            },
            'in_year_incexp': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['0200', '0400', '1000', '2000'],
                    'amount_type.code': ['ACT'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['month'],
                    'financial_year_end.year': IN_YEAR_YEARS,
                },
                'drilldown': YEAR_ITEM_DRILLDOWN + ['financial_period.period'],
                'query_type': 'aggregate',
                'results_structure': self.noop_structure,
            },
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
                'aggregate': 'total_assets.sum',
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
                'aggregate': 'total_assets.sum',
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
                'cube': 'capital',
                'aggregate': 'repairs_maintenance.sum',
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
                'cube': 'uifwexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['irregular', 'fruitless', 'unauthorised'],
                    'demarcation.code': [self.geo_code],
                    'financial_year_end.year': self.uifw_years,
                },
                'drilldown': YEAR_ITEM_DRILLDOWN,
                'query_type': 'aggregate',
                'results_structure': self.item_code_year_aggregate,
            },
            'revenue_breakdown': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': [
                        '0200',
                        '0300',
                        '0400',
                        '0700',
                        '0800',
                        '1000',
                        '1100',
                        '1300',
                        '1400',
                        '1500',
                        '1600',
                        '1610',
                        '1700',
                        '1800',
                        '1900',
                    ],
                    'amount_type.code': ['AUDA', 'ORGB'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                    'financial_year_end.year': self.years + [self.budget_year],
                },
                'drilldown': YEAR_ITEM_DRILLDOWN + ['item.label', 'amount_type.code'],
                'query_type': 'aggregate',
                'results_structure': self.noop_structure,
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
                'order': 'financial_year_end.year:desc,function.category_label:asc',
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
                'order': 'role',
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
            # For audit opinions, null results mean the opinion PDF
            # wasn't available when the dataset was updated, even if
            # we return a row for the municipality and date. Therefore
            # it's fine to let nulls go through as null to the frontend
            # unlike the numeric information
            'audit_opinions': {
                'cube': 'audit_opinions',
                'cut': {
                    'demarcation.code': [self.geo_code],
                    'financial_year_end.year': AUDIT_OPINION_YEARS[:4],
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
                'order': 'financial_year_end.year:desc',
            },
            'disestablished': {
                'cube': 'demarcation_changes',
                'cut': {
                    'old_demarcation.code': [self.geo_code],
                    'old_code_transition.code': ['disestablished'],
                },
                'fields': [
                    'new_demarcation.code',
                    'date.date'
                ],
                'value_label': '',
                'query_type': 'facts',
                'results_structure': self.noop_structure,
                'order': 'date.date:asc',
            },
            'established': {
                'cube': 'demarcation_changes',
                'cut': {
                    'new_demarcation.code': [self.geo_code],
                    'new_code_transition.code': ['established'],
                },
                'fields': [
                    'old_demarcation.code',
                    'date.date'
                ],
                'value_label': '',
                'query_type': 'facts',
                'results_structure': self.noop_structure,
                'order': 'date.date:asc',
            },
            'demarcation_involved_old': {
                'cube': 'demarcation_changes',
                'cut': {
                    'old_demarcation.code': [self.geo_code],
                    'old_code_transition.code': ['continue'],
                },
                'fields': [
                    'new_code_transition.code',
                    'new_demarcation.code',
                    'date.date'
                ],
                'value_label': '',
                'query_type': 'facts',
                'results_structure': self.noop_structure,
                'order': 'date.date:asc',
            },
            'demarcation_involved_new': {
                'cube': 'demarcation_changes',
                'cut': {
                    'new_demarcation.code': [self.geo_code],
                    'new_code_transition.code': ['continue'],
                },
                'fields': [
                    'old_code_transition.code',
                    'old_demarcation.code',
                    'date.date'
                ],
                'value_label': '',
                'query_type': 'facts',
                'results_structure': self.noop_structure,
                'order': 'date.date:asc',
            },
        }


def get_indicator_calculators(has_comparisons=None):
    calculators = [
        CashCoverage,
        OperatingBudgetDifference,
        CapitalBudgetDifference,
        RepairsMaintenance,
        RevenueSources,
        RevenueBreakdown,
        CurrentRatio,
        LiquidityRatio,
        CurrentDebtorsCollectionRate,
        ExpenditureFunctionalBreakdown,
        ExpenditureTrendsContracting,
        ExpenditureTrendsStaff,
        CashAtYearEnd,
        FruitlWastefIrregUnauth,
    ]
    if has_comparisons is None:
        return calculators
    else:
        return [calc for calc in calculators if calc.has_comparisons == has_comparisons]


def get_indicators(api_data):
    indicators = {}

    for indicator_calc in get_indicator_calculators():
        indicators[indicator_calc.indicator_name] = indicator_calc.get_muni_specifics(api_data)

    norms = {
        'cash_at_year_end': {'good': 'x>0', 'bad': 'x<=0'},
        'cash_coverage': {'good': 'x>3', 'ave': '3>=x>1', 'bad': 'x<=1'},
        'op_budget_diff': {'good': 'abs(x)<=5', 'ave': '5<abs(x)<=15', 'bad': 'abs(x)>15'},
        'cap_budget_diff': {'good': 'abs(x)<=5', 'ave': '5<abs(x)<=15', 'bad': 'abs(x)>15'},
        'rep_maint_perc_ppe': {'good': 'abs(x)>=8', 'bad': 'abs(x)<8'},
        'wasteful_exp': {'good': 'x=0', 'bad': 'x!=0'},
    }

    return indicators


class IndicatorCalculator:
    pass


class CashCoverage(IndicatorCalculator):
    indicator_name = 'cash_coverage'
    result_type = 'months'
    noun = 'coverage'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                cash = api_data.results['cash_flow']['4200'][year]
                monthly_expenses = api_data.results['op_exp_actual']['4600'][year] / 12
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
            values.append({'date': year, 'result': result, 'rating': rating})

        return {
            'values': values,
            'ref': api_data.references['solgf'],
        }


class OperatingBudgetDifference(IndicatorCalculator):
    indicator_name = 'op_budget_diff'
    result_type = '%'
    noun = 'underspending or overspending'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                op_ex_budget = api_data.results['op_exp_budget']['4600'][year]
                op_ex_actual = api_data.results['op_exp_actual']['4600'][year]
                result = percent((op_ex_actual - op_ex_budget), op_ex_budget, 1)
                overunder = 'under' if result < 0 else 'over'
                if abs(result) <= 5:
                    rating = 'good'
                elif abs(result) <= 15:
                    rating = 'ave'
                elif abs(result) > 15:
                    rating = 'bad'
                else:
                    rating = None
            except KeyError:
                result = None
                rating = None
                overunder = None
            values.append({
                'date': year,
                'result': result,
                'overunder': overunder,
                'rating': rating
            })

        return {
            'values': values,
            'ref': api_data.references['overunder'],
        }


class CapitalBudgetDifference(IndicatorCalculator):
    indicator_name = 'cap_budget_diff'
    result_type = '%'
    noun = 'underspending or overspending'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                cap_ex_budget = api_data.results['cap_exp_budget']['4100'][year]
                cap_ex_actual = api_data.results['cap_exp_actual']['4100'][year]
                result = percent((cap_ex_actual - cap_ex_budget), cap_ex_budget)
                overunder = 'under' if result < 0 else 'over'
                if abs(result) <= 5:
                    rating = 'good'
                elif abs(result) <= 15:
                    rating = 'ave'
                elif abs(result) > 15:
                    rating = 'bad'
                else:
                    rating = None
            except KeyError:
                result = None
                rating = None
                overunder = None
            values.append({
                'date': year,
                'result': result,
                'overunder': overunder,
                'rating': rating
            })

        return {
            'values': values,
            'ref': api_data.references['overunder'],
        }


class RepairsMaintenance(IndicatorCalculator):
    indicator_name = 'rep_maint_perc_ppe'
    result_type = '%'
    noun = 'spending'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                rep_maint = api_data.results['rep_maint']['4100'][year]
                ppe = api_data.results['ppe']['1300'][year]
                invest_prop = api_data.results['invest_prop']['1401'][year]
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

            values.append({'date': year, 'result': result, 'rating': rating})

        return {
            'values': values,
            'ref': api_data.references['circular71'],
        }


class RevenueSources(IndicatorCalculator):
    indicator_name = 'revenue_sources'
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        year = api_data.years[0]
        results = {
            'local': {
                'amount': 0,
                'items': [],
                },
            'government': {
                'amount': 0,
                'items': [],
                },
            'year': year,
            'ref': api_data.references['lges'],
        }
        code_to_source = {
            '0200': 'local',
            '0300': 'local',
            '0400': 'local',
            '0700': 'local',
            '0800': 'local',
            '1000': 'local',
            '1100': 'local',
            '1300': 'local',
            '1400': 'local',
            '1500': 'local',
            '1600': 'government',
            '1610': 'government',
            '1700': 'local',
            '1800': 'local',
        }
        total = None
        for item in api_data.results['revenue_breakdown']:
            if item['financial_year_end.year'] != year:
                continue
            if item['amount_type.code'] != 'AUDA':
                continue
            if item['item.code'] == '1900':
                total = item['amount.sum']
                continue
            amount = item['amount.sum']
            results[code_to_source[item['item.code']]]['amount'] += amount
            results[code_to_source[item['item.code']]]['items'].append(item)
        if total is None:
            results['government']['percent'] = None
            results['government']['value'] = None
            results['local']['percent'] = None
            results['local']['value'] = None
            results['rating'] = 'bad'
        else:
            results['government']['percent'] = percent(results['government']['amount'], total)
            local_pct = percent(results['local']['amount'], total)
            results['local']['percent'] = local_pct
            if local_pct >= 75:
                results['rating'] = 'good'
            elif local_pct >= 50:
                results['rating'] = 'ave'
            else:
                results['rating'] = 'bad'
        return results


class RevenueBreakdown(IndicatorCalculator):
    indicator_name = 'revenue_breakdown'
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        groups = [
            ('Property rates', ['0200', '0300']),
            ('Service Charges', ['0400']),
            ('Rental income', ['0700']),
            ('Interest and investments', ['0800', '1000', '1100']),
            ('Fines', ['1300']),
            ('Licenses and Permits', ['1400']),
            ('Agency services', ['1500']),
            ('Government Transfers for Operating Expenses', ['1600']),
            ('Government Transfers for Capital Expenses', ['1610']),
            ('Other', ['1700', '1800']),
        ]
        results = {}
        # Structure as {'2015': {'1900': {'AUDA': ..., 'ORGB': ...}, '0200': ...}, '2016': ...}
        for item in api_data.results['revenue_breakdown']:
            if item['financial_year_end.year'] not in results:
                results[item['financial_year_end.year']] = {}
            if item['item.code'] not in results[item['financial_year_end.year']]:
                results[item['financial_year_end.year']][item['item.code']] = {}
            results[item['financial_year_end.year']][item['item.code']][item['amount_type.code']] \
                = item
        values = []
        for year in api_data.years + [api_data.budget_year]:
            if year == api_data.budget_year:
                year_name = "%s budget" % year
                amount_type = 'ORGB'
            else:
                year_name = "%d" % year
                amount_type = 'AUDA'
            try:
                total = results[year]['1900'][amount_type]['amount.sum']
                for (label, codes) in groups:
                    amount = 0
                    for code in codes:
                        amount += results[year][code][amount_type]['amount.sum']
                    values.append({
                        'item': label,
                        'amount': amount,
                        'percent': percent(amount, total) if amount else 0,
                        'date': year_name,
                        'amount_type': amount_type,
                    })
            except KeyError:
                values.append({
                    'item': None,
                    'amount': None,
                    'percent': None,
                    'date': year_name,
                    'amount_type': amount_type,
                })

        return {'values': values}


class CurrentRatio(IndicatorCalculator):
    indicator_name = 'current_ratio'
    result_type = 'ratio'
    noun = 'ratio'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        results = api_data.results['in_year_bsheet']
        year_month_key = lambda r: (r['financial_year_end.year'], r['financial_period.period'])
        year_month_sorted = sorted(results, key=year_month_key, reverse=True)
        quarters = {}
        latest_quarter = None
        # Loop over months that exist and use their values in quarters
        for (year, month), yearmonthgroup in groupby(year_month_sorted, year_month_key):
            monthitems = list(yearmonthgroup)
            quarter_key = quarter_tuple(year, month)
            try:
                # Rely on index out of range for missing values to skip month if one's missing
                assets = [m['amount.sum'] for m in monthitems
                          if m['item.code'] == '2150'
                          and m['financial_period.period'] == month][0]
                liabilities = [m['amount.sum'] for m in monthitems
                               if m['item.code'] == '1600'
                               and m['financial_period.period'] == month][0]
                # Add a quarter the first time a month in the quarter is seen.
                # Skip the remaining months in that quarter. Thus the latest
                # month in the quarter is used.
                if quarter_key not in quarters:
                    result = ratio(assets, liabilities)
                    q = {
                        'date': quarter_string(year, month),
                        'year': year,
                        'month': month,
                        'amount_type': 'ACT',
                        'quarter': quarter_idx(month),
                        'assets': assets,
                        'liabilities': liabilities,
                        'result': result,
                        'rating': 'good' if result >= 1.5 else 'ave' if result >= 1 else 'bad',
                    }
                    quarters[quarter_key] = q
                    if latest_quarter is None:
                        latest_quarter = q
            except IndexError:
                pass
        # Enumerate the quarter keys we can expect to exist based on the latest
        # If latest is missing, there are none to show.
        if latest_quarter is not None:
            keys = []
            for q in range(latest_quarter['quarter'], 0, -1):
                keys.append((latest_quarter['year'], q))
            for q in range(4, 0, -1):
                keys.append((latest_quarter['year']-1, q))
            values = [quarters.get(k, {'year': k[0],
                                       'date': "%sq%s" % k,
                                       'quarter': k[1],
                                       'result': None,
                                       'rating': 'bad',
            }) for k in keys][:5]
        return {
            'values': values,
            'ref': api_data.references['circular71'],
        }


class LiquidityRatio(IndicatorCalculator):
    indicator_name = 'liquidity_ratio'
    result_type = 'ratio'
    noun = 'ratio'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        results = api_data.results['in_year_bsheet']
        year_month_key = lambda r: (r['financial_year_end.year'], r['financial_period.period'])
        year_month_sorted = sorted(results, key=year_month_key, reverse=True)
        quarters = {}
        latest_quarter = None
        # Loop over months that exist and use their values in quarters
        for (year, month), yearmonthgroup in groupby(year_month_sorted, year_month_key):
            monthitems = list(yearmonthgroup)
            quarter_key = quarter_tuple(year, month)
            try:
                # Rely on index out of range for missing values to skip month if one's missing
                cash = [m['amount.sum'] for m in monthitems
                          if m['item.code'] == '1800'
                          and m['financial_period.period'] == month][0]
                call_investment_deposits = [m['amount.sum'] for m in monthitems
                                            if m['item.code'] == '2200'
                                            and m['financial_period.period'] == month][0]
                liabilities = [m['amount.sum'] for m in monthitems
                               if m['item.code'] == '1600'
                               and m['financial_period.period'] == month][0]
                # Add a quarter the first time a month in the quarter is seen.
                # Skip the remaining months in that quarter. Thus the latest
                # month in the quarter is used.
                if quarter_key not in quarters:
                    result = ratio(cash + call_investment_deposits, liabilities)
                    q = {
                        'date': quarter_string(year, month),
                        'year': year,
                        'month': month,
                        'amount_type': 'ACT',
                        'quarter': quarter_idx(month),
                        'cash': cash,
                        'call_investment_deposits': call_investment_deposits,
                        'liabilities': liabilities,
                        'result': result,
                        'rating': 'good' if result >= 1 else 'bad',
                    }
                    quarters[quarter_key] = q
                    if latest_quarter is None:
                        latest_quarter = q
            except IndexError:
                pass
        # Enumerate the quarter keys we can expect to exist based on the latest
        # If latest is missing, there are none to show.
        if latest_quarter is not None:
            keys = []
            for q in range(latest_quarter['quarter'], 0, -1):
                keys.append((latest_quarter['year'], q))
            for q in range(4, 0, -1):
                keys.append((latest_quarter['year']-1, q))
            values = [quarters.get(k, {'year': k[0],
                                       'date': "%sq%s" % k,
                                       'quarter': k[1],
                                       'result': None,
                                       'rating': 'bad',
            }) for k in keys][:5]
        return {
            'values': values,
            'ref': api_data.references['mbrr'],
        }


class CurrentDebtorsCollectionRate(IndicatorCalculator):
    indicator_name = 'current_debtors_collection_rate'
    result_type = '%'
    noun = 'rate'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        results = {}
        year_month_key = lambda r: (r['financial_year_end.year'], r['financial_period.period'])
        year_month_sorted = sorted(api_data.results['in_year_cflow'], key=year_month_key, reverse=True)
        for (year, month), yearmonthgroup in groupby(year_month_sorted, year_month_key):
            results[(year, month)] = {'cflow': {}}
            for cell in yearmonthgroup:
                results[(year, month)]['cflow'][cell['item.code']] = cell['amount.sum']
        year_month_sorted = sorted(api_data.results['in_year_incexp'], key=year_month_key, reverse=True)
        for (year, month), yearmonthgroup in groupby(year_month_sorted, year_month_key):
            results[(year, month)]['incexp'] = {}
            for cell in yearmonthgroup:
                results[(year, month)]['incexp'][cell['item.code']] = cell['amount.sum']
        quarters = {}
        latest_quarter = None
        # Loop over months that exist and use their values in quarters

        for (year, month) in sorted(results.keys(), reverse=True):
            quarter_key = quarter_tuple(year, month)

            monthcells = results[(year, month)]
            try:
                # Rely on index out of range for missing values to skip month if one's missing
                # Rely on KeyError for missing values to skip month if one's missing
                 # property rates
                receipts = monthcells['cflow']['3010'] + \
                           monthcells['cflow']['3030'] + \
                           monthcells['cflow']['3040'] + \
                           monthcells['cflow']['3050'] + \
                           monthcells['cflow']['3060'] + \
                           monthcells['cflow']['3070'] + \
                           monthcells['cflow']['3100']
                billing = monthcells['incexp']['0200'] + \
                          monthcells['incexp']['0400'] + \
                          monthcells['incexp']['1000'] - \
                          monthcells['incexp']['2000']
                # Add a quarter the first time a month in the quarter is seen.
                # Assume initially that it won't be complete and thus have no
                # result and bad rating. This gets changed below if it's complete.
                if quarter_key not in quarters:
                    q = {
                        'date': quarter_string(year, month),
                        'year': year,
                        'month': month,
                        'amount_type': 'ACT',
                        'quarter': quarter_idx(month),
                        'receipts': [receipts],
                        'billing': [billing],
                        'result': None,
                        'rating': 'bad',
                    }
                    quarters[quarter_key] = q
                    if latest_quarter is None:
                        latest_quarter = q
                else:
                    quarters[quarter_key]['receipts'].append(receipts)
                    quarters[quarter_key]['billing'].append(billing)
            except KeyError as e:
                logger.debug(e)

        # Enumerate the quarter keys we can expect to exist based on the latest
        # If latest is missing, there are none to show.
        if latest_quarter is not None:
            keys = []
            for q in range(latest_quarter['quarter'], 0, -1):
                keys.append((latest_quarter['year'], q))
            for q in range(4, 0, -1):
                keys.append((latest_quarter['year']-1, q))
            for k in keys[:5]:
                q = quarters.get(k, {'year': k[0],
                                     'date': "%sq%s" % k,
                                     'quarter': k[1],
                                     'result': None,
                                     'rating': 'bad',
                                     'receipts': None,
                                     'billing': None,
                })
                if q['receipts'] and q['billing'] and len(q['receipts']) == 3 and len(q['billing']) == 3:
                    q['result'] = percent(sum(q['receipts']), sum(q['billing']))
                    q['rating'] = 'good' if round(q['result']) >= 95 else 'bad'
                values.append(q)
        return {
            'values': values,
            'ref': api_data.references['mbrr'],
        }


class ExpenditureTrendsContracting(IndicatorCalculator):
    indicator_name = 'expenditure_trends_contracting'
    result_type = '%'
    noun = 'expenditure'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []

        for year in api_data.years:
            try:
                total = api_data.results['expenditure_breakdown']['4600'][year]
            except KeyError:
                total = None

            try:
                contracting = percent(api_data.results['expenditure_breakdown']['4200'][year], total)
            except KeyError:
                contracting = None

            values.append({
                'date': year,
                'result': contracting,
                'rating': '',
            })

        return {'values': values}


class ExpenditureTrendsStaff(IndicatorCalculator):
    indicator_name = 'expenditure_trends_staff'
    result_type = '%'
    noun = 'expenditure'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []

        for year in api_data.years:
            try:
                total = api_data.results['expenditure_breakdown']['4600'][year]
            except KeyError:
                total = None

            try:
                staff = percent(api_data.results['expenditure_breakdown']['3000'][year] +
                                api_data.results['expenditure_breakdown']['3100'][year],
                                total)
            except KeyError:
                staff = None

            values.append({
                'date': year,
                'result': staff,
                'rating': '',
            })

        return {'values': values}


class ExpenditureFunctionalBreakdown(IndicatorCalculator):
    indicator_name = 'expenditure_functional_breakdown'
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        GAPD_categories = {
            'Budget & Treasury Office',
            'Executive & Council',
            'Planning and Development',
            'Corporate Services',
        }
        GAPD_label = 'Governance, Administration, Planning and Development'

        results = api_data.results['expenditure_functional_breakdown']
        grouped_results = []

        for year, yeargroup in groupby(results, lambda r: r['financial_year_end.year']):
            try:
                # Skip an entire year if total is missing, suggesting the year is missing
                total = api_data.results['expenditure_breakdown']['4600'][year]
                GAPD_total = 0.0
                year_name = "%d" % year if year != api_data.budget_year else ("%s budget" % year)

                for result in yeargroup:
                    # only do budget for budget year, use AUDA for others
                    if api_data.check_budget_actual(year, result['amount_type.code']):
                        if result['function.category_label'] in GAPD_categories:
                            GAPD_total += (result['amount.sum'])
                        else:
                            grouped_results.append({
                                'amount': result['amount.sum'],
                                'percent': percent(result['amount.sum'], total),
                                'item': result['function.category_label'],
                                'date': year_name,
                            })

                grouped_results.append({
                    'amount': GAPD_total,
                    'percent': percent(GAPD_total, total),
                    'item': GAPD_label,
                    'date': year_name,
                })
            except KeyError:
                continue

        grouped_results = sorted(grouped_results, key=lambda r: (r['date'], r['item']))
        return {'values': grouped_results}


class CashAtYearEnd(IndicatorCalculator):
    indicator_name = 'cash_at_year_end'
    result_type = 'R'
    noun = 'cash balance'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                result = api_data.results['cash_flow']['4200'][year]

                if result > 0:
                    rating = 'good'
                elif result <= 0:
                    rating = 'bad'
                else:
                    rating = None

                values.append({'date': year, 'result': result, 'rating': rating})
            except KeyError:
                values.append({'date': year, 'result': None, 'rating': 'bad'})
        return {
            'values': values,
            'ref': api_data.references['solgf'],
        }


class FruitlWastefIrregUnauth(IndicatorCalculator):
    indicator_name = 'wasteful_exp'
    result_type = '%'
    noun = 'expenditure'
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        aggregate = {}
        for item, results in api_data.results['wasteful_exp'].items():
            for year, amount in results.items():
                if year in aggregate:
                    aggregate[year] += amount
                else:
                    aggregate[year] = amount

        for year in api_data.uifw_years:
            try:
                op_ex_actual = api_data.results['op_exp_actual']['4600'][year]
                result = percent(aggregate[year], op_ex_actual)
                rating = None
                if result == 0:
                    rating = 'good'
                else:
                    rating = 'bad'
            except KeyError:
                result = None
                rating = None

            values.append({'date': year, 'result': result, 'rating': rating})

        return {
            'values': values,
            'ref': api_data.references['circular71'],
        }


class Demarcation(object):

    def __init__(self, api_data):
        self.land_gained = []
        self.land_lost = []
        self.disestablished = False
        self.established_after_last_audit = False
        self.established_within_audit_years = False
        date_key = lambda x: x['date.date']
        # Watch out: groupby's iterator is finicky about seeing things twice.
        # E.g. If you just turn the tuples iterator into a list you only see one
        # item in the group
        for date, group in groupby(api_data.results['disestablished'], date_key):
            if self.disestablished:
                # If this is the second iteration
                raise Exception("Muni disestablished more than once")
            else:
                self.disestablished = True
                self.disestablished_date = date
                self.disestablished_to = [x['new_demarcation.code'] for x in group]
        for date, group in groupby(api_data.results['established'], date_key):
            if self.established_after_last_audit:
                # If this is the second iteration
                raise Exception("Muni established more than once")
            else:
                datetime = dateutil.parser.parse(date)
                year, month = calendar_to_financial(datetime.year, datetime.month)
                quarter = quarter_string(year, month)
                if quarter > LAST_AUDIT_QUARTER:
                    self.established_after_last_audit = True
                if datetime.year in api_data.years:
                    self.established_within_audit_years = True
                self.established_date = date
                self.established_from = [x['old_demarcation.code'] for x in group]
        for date, group in groupby(api_data.results['demarcation_involved_new'], date_key):
            self.land_gained.append({
                'date': date,
                'changes': [{
                    'change': x['old_code_transition.code'],
                    'demarcation_code': x['old_demarcation.code']
                } for x in group]})
        for date, group in groupby(api_data.results['demarcation_involved_old'], date_key):
            self.land_lost.append({
                'date': date,
                'changes': [{
                    'change': x['new_code_transition.code'],
                    'demarcation_code': x['new_demarcation.code']
                } for x in group]})

    def as_dict(self):
        demarcation_dict = {
            'land_gained': self.land_gained,
            'land_lost': self.land_lost,
        }
        if self.disestablished:
            demarcation_dict.update({
                'disestablished': True,
                'disestablished_date': self.disestablished_date,
                'disestablished_to': self.disestablished_to,
            })
        if self.established_after_last_audit or self.established_within_audit_years:
            demarcation_dict.update({
                'established_after_last_audit': self.established_after_last_audit,
                'established_within_audit_years': self.established_within_audit_years,
                'established_date': self.established_date,
                'established_from': self.established_from,
            })
        return demarcation_dict


def calendar_to_financial(year, month):
    """
    2016 8 -> 2017 2
    2016 6 -> 2016 12
    2016 3 -> 2016 9
    """
    if month > 6:
        year += 1
    month = (month + 6) % 12
    if month == 0:
        month = 12
    return year, month


def quarter_idx(month):
    return ((month - 1) // 3) + 1


def quarter_tuple(year, month):
    return (year, quarter_idx(month))


def quarter_string(year, month):
    return "%sq%s" % quarter_tuple(year, month)
