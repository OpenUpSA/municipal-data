import requests
from collections import defaultdict, OrderedDict

from wazimap.data.utils import percent, ratio

class MuniApiClient(object):
    def __init__(self, geo_code):
        self.API_URL = 'https://data.municipalmoney.org.za/api/cubes/'
        self.geo_code = str(geo_code)
        self.query_structure = self.build_query_structure()

        self.results = defaultdict(dict)
        self.years = set()
        for line_item, query_params in self.query_structure.iteritems():
            self.results[line_item], self.years = self.get_results_from_api(query_params, self.years)

    def get_results_from_api(self, query_params, years):

      if query_params['query_type'] == 'aggregate':
          url = self.API_URL + query_params['cube'] + '/aggregate'
          params = {
              'aggregates': query_params['aggregate'],
              'cut': '|'.join('{!s}:{!s}'.format(
                  k, ';'.join('{!r}'.format(item) for item in v))
                  for (k, v) in query_params['cut'].iteritems()
              ).replace("'", '"'),
              'drilldown': 'item.code|item.label|financial_period.period',
              'page': 0,
              'order': 'financial_period.period:desc',
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

      api_response = requests.get(url, params=params, verify=False).json()

      if query_params['query_type'] == 'facts':
          if query_params['annual']:
              results, years = self.annual_facts_from_response(api_response, query_params, years)
          else:
              results = self.facts_from_response(api_response, query_params)
      else:
          results, years = self.aggregate_from_response(api_response, query_params, years)

      return results, years

    @staticmethod
    def aggregate_from_response(response, query_params, years):
        """
        Return results and years.
        Results are the values we received from the API in the following format:
        {
            '4100': {2015: 11981070609.0}, {2014: 844194485.0}, {2013: 593485329.0}
        }

        Years is a set of years in the results we received,
        used determine which periods we use when presenting results.
        """
        results = {}
        for code in query_params['cut']['item.code']:
          results[code] = OrderedDict([
              (c['financial_period.period'], c[query_params['aggregate']])
              for c in response['cells'] if c['item.code'] == code])
          years |= set([int(year) for year in results[code].keys()])

        return results, years

    @staticmethod
    def annual_facts_from_response(response, query_params, years):
        """
        Return facts that have annual results,
        and a set of years in the results we received,
        used determine which periods we use when presenting results.
        """
        facts = OrderedDict([
            (i['financial_year_end.year'], i[query_params['value_label']])
            for i in response['data']])
        years |= set([int(year) for year in facts.keys()])

        return facts, years

    @staticmethod
    def facts_from_response(response, query_params):
        return response['data']


    def build_query_structure(self):
        return {
            'op_exp_actual': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['4600'],
                    'amount_type.label': ['Audited Actual'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                },
                'query_type': 'aggregate',
            },
            'op_exp_budget': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['4600'],
                    'amount_type.label': ['Adjusted Budget'],
                    'demarcation.code': [self.geo_code],
                },
                'query_type': 'aggregate',
            },
            'cash_flow': {
                'cube': 'cflow',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['4200'],
                    'amount_type.label': ['Audited Actual'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year']
                },
                'query_type': 'aggregate',
            },
            'cap_exp_actual': {
                'cube': 'capital',
                'aggregate': 'asset_register_summary.sum',
                'cut': {
                    'item.code': ['4100'],
                    'amount_type.label': ['Audited Actual'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year']
                },
                'query_type': 'aggregate',
            },
            'cap_exp_budget': {
                'cube': 'capital',
                'aggregate': 'asset_register_summary.sum',
                'cut': {
                    'item.code': ['4100'],
                    'amount_type.label': ['Adjusted Budget'],
                    'demarcation.code': [self.geo_code],
                },
                'query_type': 'aggregate',
            },
            'rep_maint': {
                'cube': 'repmaint',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['5005'],
                    'amount_type.label': ['Audited Actual'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year']
                },
                'query_type': 'aggregate',
            },
            'ppe': {
                'cube': 'bsheet',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['1300'],
                    'amount_type.label': ['Audited Actual'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                },
                'query_type': 'aggregate',
            },
            'invest_prop': {
                'cube': 'bsheet',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['1401'],
                    'amount_type.label': ['Audited Actual'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                },
                'query_type': 'aggregate',
            },
            'revenue_breakdown': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['0200', '0400', '1600', '1700', '1900'],
                    'amount_type.label': ['Audited Actual'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                },
                'query_type': 'aggregate',
            },
            'expenditure_breakdown': {
                'cube': 'incexp',
                'aggregate': 'amount.sum',
                'cut': {
                    'item.code': ['3000', '3100', '3400', '4100', '4200', '4300', '3700', '4600'],
                    'amount_type.label': ['Audited Actual'],
                    'demarcation.code': [self.geo_code],
                    'period_length.length': ['year'],
                },
                'query_type': 'aggregate',
            },
            'officials': {
                'query_type': 'facts',
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
                'annual': False,
                'value_label': ''
            },
            'contact_details' : {
                'query_type': 'facts',
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
                'annual': False,
                'value_label': ''
            },
            'audit_opinions' : {
                'query_type': 'facts',
                'cube': 'audit_opinions',
                'cut': {
                    'municipality.demarcation_code': self.geo_code,
                },
                'fields': [
                    'opinion.code',
                    'opinion.label',
                    'financial_year_end.year'
                ],
                'annual': True,
                'value_label': 'opinion.label'
            },
        }


class IndicatorCalculator(object):
    def __init__(self, results, years):
        self.results = results
        self.years = years

        self.revenue_breakdown_items = [
            ('property_rates', '0200'),
            ('service_charges', '0400'),
            ('transfers_received', '1600'),
            ('own_revenue', '1700'),
            ('total', '1900')
        ]

        self.expenditure_breakdown_items = [
            ('employee_related_costs', ['3000', '3100']),
            ('councillor_remuneration', '3400'),
            ('bulk_purchases', '4100'),
            ('contracted_services', '4200'),
            ('transfers_spent', '4300'),
            ('depreciation_amortisation', '3700'),
            ('total', '4600')
        ]

    def cash_coverage(self):
        values = OrderedDict()
        for year in sorted(list(self.years), reverse=True):
            try:
                values[year] = ratio(
                    self.results['cash_flow']['4200'][year],
                    (self.results['op_exp_actual']['4600'][year] / 12),
                    1)
            except KeyError:
                values[year] = None

        return values

    def op_budget_diff(self):
        values = OrderedDict()
        for year in sorted(list(self.years), reverse=True):
            try:
                values[year] = percent(
                    (self.results['op_exp_budget']['4600'][year] - self.results['op_exp_actual']['4600'][year]),
                    self.results['op_exp_budget']['4600'][year],
                    1)
            except KeyError:
                values[year] = None

        return values

    def cap_budget_diff(self):
        values = OrderedDict()
        for year in sorted(list(self.years), reverse=True):
            try:
                values[year] = percent(
                    (self.results['cap_exp_budget']['4100'][year] - self.results['cap_exp_actual']['4100'][year]),
                    self.results['cap_exp_budget']['4100'][year])
            except KeyError:
                values[year] = None

        return values

    def rep_maint_perc_ppe(self):
        values = OrderedDict()
        for year in sorted(list(self.years), reverse=True):
            try:
                values[year] = percent(self.results['rep_maint']['5005'][year],
                (self.results['ppe']['1300'][year] + self.results['invest_prop']['1401'][year]))
            except KeyError:
                values[year] = None

        return values

    def revenue_breakdown(self):
        values = OrderedDict()
        for year in sorted(list(self.years), reverse=True):
            values[year] = {}
            subtotal = 0.0
            for name, code in self.revenue_breakdown_items:
                try:
                    values[year][name] = self.results['revenue_breakdown'][code][year]
                    if not name == 'total':
                        subtotal += values[year][name]
                except KeyError:
                    values[year][name] = None

            if values[year]['total']:
                values[year]['other'] = values[year]['total'] - subtotal
            else:
                values[year]['other'] = None

        return values

    def expenditure_breakdown(self):
        values = OrderedDict()
        for year in sorted(list(self.years), reverse=True):
            values[year] = {}
            subtotal = 0.0
            for name, code in self.expenditure_breakdown_items:
                try:
                    if not type(code) is list:
                        values[year][name] = self.results['expenditure_breakdown'][code][year]
                    else:
                        values[year][name] = 0.0
                        for c in code:
                            values[year][name] += self.results['expenditure_breakdown'][c][year]
                    if not name == 'total':
                        subtotal += values[year][name]
                except KeyError:
                    values[year][name] = None

            if values[year]['total']:
                values[year]['other'] = values[year]['total'] - subtotal
            else:
                values[year]['other'] = None

        return values

    def cash_at_year_end(self):
        return OrderedDict([(k, v) for k, v in self.results['cash_flow']['4200'].iteritems()])

    def mayoral_staff(self):
        values = []
        exclude_roles = ['Speaker',  'Secretary of Speaker']

        for official in self.results['officials']:
            if not official['role.role'] in exclude_roles:
                values.append({
                    'role': official['role.role'],
                    'title': official['contact_details.title'],
                    'name': official['contact_details.name'],
                    'office_phone': official['contact_details.phone_number'],
                    'fax_number': official['contact_details.fax_number'],
                    'email': official['contact_details.email_address']
                })

        return values

    def muni_contact(self):
        muni_contact = self.results['contact_details'][0]
        values = {
            'street_address_1': muni_contact['municipality.street_address_1'],
            'street_address_2': muni_contact['municipality.street_address_2'],
            'street_address_3': muni_contact['municipality.street_address_3'],
            'street_address_4': muni_contact['municipality.street_address_4'],
            'phone_number': muni_contact['municipality.phone_number'],
            'url': muni_contact['municipality.url'].lower()
        }

        return values

    def audit_opinions(self):
        return OrderedDict(sorted(
            self.results['audit_opinions'].items(), key=lambda t: t[0],
            reverse=True))
