import sys
sys.path.append('.')

from scorecard.profile_data import IndicatorCalculator
import argparse
import json

API_URL = 'https://municipaldata.treasury.gov.za/api'

def main():
    parser = argparse.ArgumentParser(description='Tool to dump the materialised views of the municipal finance data used on the Municipal Money website.')
    parser.add_argument('-d', '--demarcation-code', required=True, help='Demarcation Code of the municipality you\'d like to dump data for.')

    args = parser.parse_args()

    indicator_calc = IndicatorCalculator(API_URL, args.demarcation_code)
    indicator_calc.fetch_data()

    indicators = {}

    indicators['cash_at_year_end'] = indicator_calc.cash_at_year_end()
    indicators['cash_coverage'] = indicator_calc.cash_coverage()
    indicators['op_budget_diff'] = indicator_calc.op_budget_diff()
    indicators['cap_budget_diff'] = indicator_calc.cap_budget_diff()
    indicators['current_ratio'] = indicator_calc.current_ratio()
    indicators['liquidity_ratio'] = indicator_calc.liquidity_ratio()
    indicators['current_debtors_collection_rate'] = indicator_calc.current_debtors_collection_rate()
    indicators['rep_maint_perc_ppe'] = indicator_calc.rep_maint_perc_ppe()
    indicators['wasteful_exp'] = indicator_calc.wasteful_exp_perc_exp()
    indicators['expenditure_trends'] = indicator_calc.expenditure_trends()
    indicators['revenue_sources'] = indicator_calc.revenue_sources()
    indicators['revenue_breakdown'] = indicator_calc.revenue_breakdown()
    indicators['expenditure_trends'] = indicator_calc.expenditure_trends()
    indicators['expenditure_functional_breakdown'] = indicator_calc.expenditure_functional_breakdown()

    print(json.dumps({
        'mayoral_staff': indicator_calc.mayoral_staff(),
        'muni_contact': indicator_calc.muni_contact(),
        'audit_opinions': indicator_calc.audit_opinions(),
        'indicators': indicators,
    }))


if __name__ == "__main__":
    main()
