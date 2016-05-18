from wazimap.data.tables import get_datatable
from profile_data import MuniApiClient, IndicatorCalc

def get_profile(geo_code, geo_level, profile_name=None):
    # Census data
    table = get_datatable('population_2011')
    _, total_pop = table.get_stat_data(geo_level, geo_code, percent=False)

    api_client = MuniApiClient(geo_code)
    indicator_calc = IndicatorCalc(api_client.results, api_client.years)

    return {
        'total_population': total_pop,
        'cash_coverage': indicator_calc.cash_coverage(),
        'op_budget_diff': indicator_calc.op_budget_diff(),
        'cap_budget_diff': indicator_calc.cap_budget_diff(),
        'rep_maint_perc_ppe': indicator_calc.rep_maint_perc_ppe(),
        'mayoral_staff': indicator_calc.mayoral_staff(),
        'muni_contact': indicator_calc.muni_contact(),
        'audit_opinions': indicator_calc.audit_opinions(),
        'cash_at_year_end': indicator_calc.cash_at_year_end(),
        'revenue_breakdown': indicator_calc.revenue_breakdown()
    }
