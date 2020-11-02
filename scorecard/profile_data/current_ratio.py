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


def translate_rating(value):
    if value >= 1.5:
        return "good"
    elif value >= 1:
        return "ave"
    else:
        return "bad"


def generate_quarter_data(key, values):
    year, quarter = key
    data = {
        "date": "%sq%s" % (year, quarter),
        "year": year,
        "quarter": quarter,
    }
    if values:
        assets = values["assets"]
        liabilities = values["liabilities"]
        result = ratio(assets, liabilities)
        data.update({
            "month": values["month"],
            "amount_type": "ACT",
            "assets": assets,
            "liabilities": liabilities,
            "result": result,
            "rating": translate_rating(result),
        })
    else:
        data.update({
            "result": None,
            "rating": "bad",
        })
    return data


class CurrentRatio(IndicatorCalculator):
    indicator_name = "current_ratio"
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
            periods[key]["assets"] = result.get("2150")
            periods[key]["liabilities"] = result.get("1600")
        # Populate periods with v2 data
        grouped_results = group_items_by_month(results["in_year_bsheet_v2"])
        for key, result in grouped_results:
            _, month = key
            periods.setdefault(key, {"month": month})
            periods[key]["assets"] = sum_item_amounts(result, [
                "0120", "0130", "0140", "0150", "0160", "0170",
            ])
            periods[key]["liabilities"] = sum_item_amounts(result, [
                "0330", "0340", "0350", "0360", "0370",
            ])
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "assets", "liabilities",
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
            "ref": api_data.references["circular71"],
        }
