from .utils import (
    ratio,
    generate_expected_quarter_keys,
    quarter_index,
    group_items_by_month,
    sum_item_amounts,
    group_quarters,
    filter_for_all_keys,
    select_latest_month,
)
from .indicator_calculator import IndicatorCalculator


def generate_quarter_data(key, values):
    year, quarter = key
    data = {
        "date": "%sq%s" % (year, quarter),
        "year": year,
        "quarter": quarter,
    }
    if values:
        month = values["month"]
        cash = values["cash"]
        call_investment_deposits = values["call_investment_deposits"]
        total_current_liabilities = values["total_current_liabilities"]
        result = ratio(
            cash + call_investment_deposits, total_current_liabilities
        )
        data.update({
            "month": month,
            "amount_type": "ACT",
            "cash": cash,
            "call_investment_deposits": call_investment_deposits,
            "liabilities": total_current_liabilities,
            "result": result,
            "rating": "good" if result >= 1 else "bad",
        })
    else:
        data.update({
            "result": None,
            "rating": "bad",
        })
    return data


class LiquidityRatio(IndicatorCalculator):
    indicator_name = "liquidity_ratio"
    result_type = "ratio"
    noun = "ratio"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
        periods = {}
        # Populate periods with v1 data
        grouped_results = group_items_by_month(results["in_year_bsheet"])
        for key, result in grouped_results:
            _, month = key
            periods.setdefault(key, {"month": month})
            periods[key]["cash"] = result.get("1800")
            periods[key]["call_investment_deposits"] = result.get("2200")
            periods[key]["total_current_liabilities"] = result.get("1600")
        # Populate periods with v2 data
        grouped_results = group_items_by_month(results["in_year_bsheet_v2"])
        for key, result in grouped_results:
            _, month = key
            periods.setdefault(key, {"month": month})
            periods[key]["cash"] = result.get("0120")
            periods[key]["call_investment_deposits"] = result.get("0130")
            periods[key]["total_current_liabilities"] = sum_item_amounts(result, [
                "0330", "0340", "0350", "0360", "0370",
            ])
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "cash",
            "call_investment_deposits",
            "total_current_liabilities",
        ])
        # Group periods by quarter and select latest month
        quarters = group_quarters(periods, select_latest_month)
        # Convert the qurters to a dictionary
        quarters = dict(quarters)
        # Compile the data for the expected quarters, starting with the latest
        values = []
        if len(quarters) > 0:
            latest_quarter_key = list(quarters.keys())[0]
            values = list(
                map(
                    lambda k: generate_quarter_data(k, quarters.get(k)),
                    generate_expected_quarter_keys(latest_quarter_key, 5)
                )
            )
        # Return the compiled data
        return {
            "values": values,
            "ref": api_data.references["mbrr"],
        }
