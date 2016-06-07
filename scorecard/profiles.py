from wazimap.data.tables import get_datatable
from profile_data import MuniApiClient, IndicatorCalculator
from wazimap.geo import geo_data


def get_profile(geo_code, geo_level, profile_name=None):
    # Census data
    table = get_datatable('population_2011')
    _, total_pop = table.get_stat_data(geo_level, geo_code, percent=False)

    geo = geo_data.get_geography(geo_code, geo_level)
    population_density = None
    if geo.square_kms:
        population_density = total_pop / geo.square_kms

    api_client = MuniApiClient(geo_code)
    indicator_calc = IndicatorCalculator(api_client.results, api_client.years)

    indicators = {}

    indicators['cash_at_year_end'] = indicator_calc.cash_at_year_end()
    indicators['cash_coverage'] = indicator_calc.cash_coverage()
    indicators['op_budget_diff'] = indicator_calc.op_budget_diff()
    indicators['cap_budget_diff'] = indicator_calc.cap_budget_diff()
    indicators['rep_maint_perc_ppe'] = indicator_calc.rep_maint_perc_ppe()
    indicators['wasteful_exp_perc_exp'] = indicator_calc.wasteful_exp_perc_exp()
    indicators['expenditure_trends'] = indicator_calc.expenditure_trends()

    return {
        'total_population': total_pop,
        'population_density': population_density,
        'mayoral_staff': indicator_calc.mayoral_staff(),
        'muni_contact': indicator_calc.muni_contact(),
        'audit_opinions': indicator_calc.audit_opinions(),
        'indicators': indicators,
        'revenue_breakdown': indicator_calc.revenue_breakdown(),
        'expenditure_functional_breakdown':
        indicator_calc.expenditure_functional_breakdown(),
    }
