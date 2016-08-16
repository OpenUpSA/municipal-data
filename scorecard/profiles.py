from wazimap.data.tables import get_datatable
from wazimap.geo import geo_data


from profile_data import IndicatorCalculator


def get_profile(geo_code, geo_level, profile_name=None):
    # Census data
    table = get_datatable('population_2011')
    _, total_pop = table.get_stat_data(geo_level, geo_code, percent=False)

    geo = geo_data.get_geography(geo_code, geo_level)
    population_density = None
    if geo.square_kms:
        population_density = total_pop / geo.square_kms

    indicator_calc = IndicatorCalculator(geo_code)
    indicator_calc.fetch_data()

    indicators = {}

    indicators['cash_at_year_end'] = indicator_calc.cash_at_year_end()
    indicators['cash_coverage'] = indicator_calc.cash_coverage()
    indicators['op_budget_diff'] = indicator_calc.op_budget_diff()
    indicators['cap_budget_diff'] = indicator_calc.cap_budget_diff()
    indicators['current_ratio'] = indicator_calc.current_ratio()
    indicators['liquidity_ratio'] = indicator_calc.liquidity_ratio()
    indicators['rep_maint_perc_ppe'] = indicator_calc.rep_maint_perc_ppe()
    indicators['wasteful_exp'] = indicator_calc.wasteful_exp_perc_exp()
    indicators['expenditure_trends'] = indicator_calc.expenditure_trends()
    indicators['revenue_sources'] = indicator_calc.revenue_sources()
    indicators['revenue_breakdown'] = indicator_calc.revenue_breakdown()
    indicators['expenditure_trends'] = indicator_calc.expenditure_trends()
    indicators['expenditure_functional_breakdown'] = indicator_calc.expenditure_functional_breakdown()

    return {
        'total_population': total_pop,
        'population_density': population_density,
        'mayoral_staff': indicator_calc.mayoral_staff(),
        'muni_contact': indicator_calc.muni_contact(),
        'audit_opinions': indicator_calc.audit_opinions(),
        'indicators': indicators,
    }
