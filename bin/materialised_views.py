import sys
sys.path.append('.')

from scorecard.profile_data import IndicatorCalculator, MuniApiClient
import argparse
import json

API_URL = 'https://municipaldata.treasury.gov.za/api'

def main():

    parser = argparse.ArgumentParser(description='Tool to dump the materialised views of the municipal finance data used on the Municipal Money website.')
    parser.add_argument('--api-url', help='API URL to use. Default: ' + API_URL)

    args = parser.parse_args()
    if args.api_url:
        api_url = args.api_url
    else:
        api_url = API_URL
    api_client = MuniApiClient(api_url)

    munis = get_munis(api_client)

    for muni in munis:
        profile = get_muni_profile(api_client, muni.get('municipality.demarcation_code'))
        muni.update(profile)

    print(json.dumps(munis))


def get_muni_profile(client, demarcation_code):
    indicator_calc = IndicatorCalculator(client.API_URL, demarcation_code, client=client)
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

    return {
        'mayoral_staff': indicator_calc.mayoral_staff(),
        'muni_contact': indicator_calc.muni_contact(),
        'audit_opinions': indicator_calc.audit_opinions(),
        'indicators': indicators,
    }


def get_munis(api_client):
    query = api_client.api_get({'query_type': 'facts',
                                 'cube': 'municipalities',
                                 'fields': [
                                     'municipality.demarcation_code',
                                     'municipality.name',
                                     'municipality.development_category',
                                 ],
                                 'value_label': '',
    })
    result = query.result()
    result.raise_for_status()
    body = result.json()
    if body.get("total_cell_count") == body.get("page_size"):
        raise Exception("should page municipalities")
    return body.get("data")



if __name__ == "__main__":
    main()
