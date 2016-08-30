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
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from collections import defaultdict, OrderedDict
import dateutil.parser
from itertools import groupby
from datetime import datetime
import logging
import urllib

from django.conf import settings

from wazimap.data.utils import percent, ratio

logger = logging.getLogger('municipal_finance')

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

        logger.debug("API query %s?%s" % (url, urllib.urlencode(params)))
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
        }

    def fetch_data(self):
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
            values.append({'date': year, 'result': result, 'rating': rating})

        return {
            'values': values,
            'ref': self.references['solgf'],
        }

    def op_budget_diff(self):
        values = []
        for year in self.years:
            try:
                op_ex_budget = self.results['op_exp_budget']['4600'][year]
                op_ex_actual = self.results['op_exp_actual']['4600'][year]
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
            'ref': self.references['overunder'],
        }

    def cap_budget_diff(self):
        values = []
        for year in self.years:
            try:
                cap_ex_budget = self.results['cap_exp_budget']['4100'][year]
                cap_ex_actual = self.results['cap_exp_actual']['4100'][year]
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
            'ref': self.references['overunder'],
        }

    def rep_maint_perc_ppe(self):
        values = []
        for year in self.years:
            try:
                rep_maint = self.results['rep_maint']['4100'][year]
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

            values.append({'date': year, 'result': result, 'rating': rating})

        return {
            'values': values,
            'ref': self.references['circular71'],
        }

    def revenue_sources(self):
        year = self.years[0]
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
        for item in self.results['revenue_breakdown']:
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

    def revenue_breakdown(self):
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
        for item in self.results['revenue_breakdown']:
            if item['financial_year_end.year'] not in results:
                results[item['financial_year_end.year']] = {}
            if item['item.code'] not in results[item['financial_year_end.year']]:
                results[item['financial_year_end.year']][item['item.code']] = {}
            results[item['financial_year_end.year']][item['item.code']][item['amount_type.code']] \
                = item
        values = []
        for year in self.years + [self.budget_year]:
            if year == self.budget_year:
                year_name = "%s budget" % year
                amount_type = 'ORGB'
            else:
                year_name = year
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

    def current_ratio(self):
        values = []
        results = self.results['in_year_bsheet']
        year_month_key = lambda r: (r['financial_year_end.year'], r['financial_period.period'])
        year_month_sorted = sorted(results, key=year_month_key, reverse=True)
        quarters = {}
        latest_quarter = None
        # Loop over months that exist and use their values in quarters
        for (year, month), yearmonthgroup in groupby(year_month_sorted, year_month_key):
            monthitems = list(yearmonthgroup)
            quarter_idx = ((month - 1) / 3) + 1
            quarter_key = (year, quarter_idx)
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
                        'date': "%sq%s" % quarter_key,
                        'year': year,
                        'month': month,
                        'amount_type': 'ACT',
                        'quarter': quarter_idx,
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
            for q in xrange(latest_quarter['quarter'], 0, -1):
                keys.append((latest_quarter['year'], q))
            for q in xrange(4, 0, -1):
                keys.append((latest_quarter['year']-1, q))
            values = [quarters.get(k, {'year': k[0],
                                       'date': "%sq%s" % k,
                                       'quarter': k[1],
                                       'result': None,
                                       'rating': 'bad',
            }) for k in keys][:5]
        return {
            'values': values,
            'ref': self.references['circular71'],
        }

    def liquidity_ratio(self):
        values = []
        results = self.results['in_year_bsheet']
        year_month_key = lambda r: (r['financial_year_end.year'], r['financial_period.period'])
        year_month_sorted = sorted(results, key=year_month_key, reverse=True)
        quarters = {}
        latest_quarter = None
        # Loop over months that exist and use their values in quarters
        for (year, month), yearmonthgroup in groupby(year_month_sorted, year_month_key):
            monthitems = list(yearmonthgroup)
            quarter_idx = ((month - 1) / 3) + 1
            quarter_key = (year, quarter_idx)
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
                        'date': "%sq%s" % quarter_key,
                        'year': year,
                        'month': month,
                        'amount_type': 'ACT',
                        'quarter': quarter_idx,
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
            for q in xrange(latest_quarter['quarter'], 0, -1):
                keys.append((latest_quarter['year'], q))
            for q in xrange(4, 0, -1):
                keys.append((latest_quarter['year']-1, q))
            values = [quarters.get(k, {'year': k[0],
                                       'date': "%sq%s" % k,
                                       'quarter': k[1],
                                       'result': None,
                                       'rating': 'bad',
            }) for k in keys][:5]
        return {
            'values': values,
            'ref': '',
        }

    def current_debtors_collection_rate(self):
        values = []
        results = {}
        year_month_key = lambda r: (r['financial_year_end.year'], r['financial_period.period'])
        year_month_sorted = sorted(self.results['in_year_cflow'], key=year_month_key, reverse=True)
        for (year, month), yearmonthgroup in groupby(year_month_sorted, year_month_key):
            results[(year, month)] = {'cflow': {}}
            for cell in yearmonthgroup:
                results[(year, month)]['cflow'][cell['item.code']] = cell['amount.sum']
        year_month_sorted = sorted(self.results['in_year_incexp'], key=year_month_key, reverse=True)
        for (year, month), yearmonthgroup in groupby(year_month_sorted, year_month_key):
            results[(year, month)]['incexp'] = {}
            for cell in yearmonthgroup:
                results[(year, month)]['incexp'][cell['item.code']] = cell['amount.sum']
        quarters = {}
        latest_quarter = None
        # Loop over months that exist and use their values in quarters

        for (year, month) in sorted(results.keys(), reverse=True):
            quarter_idx = ((month - 1) / 3) + 1
            quarter_key = (year, quarter_idx)

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
                        'date': "%sq%s" % quarter_key,
                        'year': year,
                        'month': month,
                        'amount_type': 'ACT',
                        'quarter': quarter_idx,
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
            except KeyError, e:
                logger.debug(e)

        # Enumerate the quarter keys we can expect to exist based on the latest
        # If latest is missing, there are none to show.
        if latest_quarter is not None:
            keys = []
            for q in xrange(latest_quarter['quarter'], 0, -1):
                keys.append((latest_quarter['year'], q))
            for q in xrange(4, 0, -1):
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
                if len(q['receipts']) == 3 and len(q['billing']) == 3:
                    q['result'] = percent(sum(q['receipts']), sum(q['billing']))
                    q['rating'] = 'good' if round(q['result']) >= 100 else 'bad'
                values.append(q)
        return {
            'values': values,
            'ref': '',
        }

    def expenditure_trends(self):
        values = {
            'staff': {'values': []},
            'contracting': {'values': []},
        }

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

            values['staff']['values'].append({
                'date': year,
                'result': staff,
                'rating': '',
            })

            try:
                contracting = percent(self.results['expenditure_breakdown']['4200'][year], total)
            except KeyError:
                contracting = None

            values['contracting']['values'].append({
                'date': year,
                'result': contracting,
                'rating': '',
            })

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
                # Skip an entire year if total is missing, suggesting the year is missing
                total = self.results['expenditure_breakdown']['4600'][year]
                GAPD_total = 0.0
                year_name = year if year != self.budget_year else ("%s budget" % year)

                for result in yeargroup:
                    # only do budget for budget year, use AUDA for others
                    if self.check_budget_actual(year, result['amount_type.code']):
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

    def cash_at_year_end(self):
        values = []
        for year in self.years:
            try:
                result = self.results['cash_flow']['4200'][year]

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
            'ref': self.references['solgf'],
        }

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

            values.append({'date': year, 'result': result, 'rating': rating})

        return {
            'values': values,
            'ref': self.references['circular71'],
        }

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
        today = datetime.now()
        in_year_years = [today.year, today.year-1, today.year-2]
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
                    'financial_year_end.year': in_year_years,
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
                    'financial_year_end.year': in_year_years,
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
                    'financial_year_end.year': in_year_years,
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
            # For audit opinions, null results mean the opinion PDF
            # wasn't available when the dataset was updated, even if
            # we return a row for the municipality and date. Therefore
            # it's fine to let nulls go through as null to the frontend
            # unlike the numeric information
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
