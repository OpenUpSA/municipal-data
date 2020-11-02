from functools import reduce

from .utils import (
    percent,
    group_items_by_month,
    sum_item_amounts,
    group_quarters,
    generate_expected_quarter_keys,
    filter_for_all_keys,
)
from .indicator_calculator import IndicatorCalculator


def sum_all_keys(result, obj):
    for key, value in obj.items():
        current = result.setdefault(key, 0)
        result[key] = current + value
    return result


def sum_all_months(item):
    key, months = item
    # Remove keys
    months = list(map(lambda o: o[1], months))
    # Only include quarters with all three months
    if len(months) < 3:
        return (key, None)
    # Calculate and return result
    return (key, reduce(sum_all_keys, months, {}))


def generate_quarter_data(key, values):
    year, quarter = key
    data = {
        "year": year,
        "date": "%sq%s" % (year, quarter),
        "quarter": quarter,

    }
    if values:
        collected_revenue = values["collected_revenue"]
        billed_revenue = values["billed_revenue"]
        result = percent(collected_revenue, billed_revenue)
        data.update({
            "month": values["month"],
            "amount_type": "ACT",
            "receipts": [collected_revenue],
            "billing": [billed_revenue],
            "result": result,
            "rating": "good" if round(result) >= 95 else "bad",
        })
    else:
        data.update({
            "result": None,
            "rating": "bad",
            "receipts": None,
            "billing": None,
        })
    return data


class CurrentDebtorsCollectionRate(IndicatorCalculator):
    indicator_name = "current_debtors_collection_rate"
    result_type = "%"
    noun = "rate"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
        periods = {}
        # Populate periods with v1 cash flow data
        grouped_results = group_items_by_month(results["in_year_cflow"])
        for key, result in grouped_results:
            _, month = key
            periods.setdefault(key, {"month": month})
            periods[key]["collected_revenue"] = sum_item_amounts(result, [
                "3010", "3030", "3040", "3050", "3060", "3070", "3100",
            ])
        # Populate periods with v1 income and expenditure data
        grouped_results = group_items_by_month(results["in_year_incexp"])
        for key, result in grouped_results:
            _, month = key
            periods.setdefault(key, {"month": month})
            periods[key]["billed_revenue"] = sum_item_amounts(result, [
                "0200", "0400", "1000",
            ]) - result.get("2000", 0)
        # Populate periods with v2 cash flow data
        grouped_results = group_items_by_month(results["in_year_cflow_v2"])
        for key, result in grouped_results:
            _, month = key
            periods.setdefault(key, {"month": month})
            periods[key]["collected_revenue"] = sum_item_amounts(result, [
                "0120", "0130", "0170",
            ])
        # Populate periods with v2 income and expenditure data
        grouped_results = group_items_by_month(results["in_year_incexp_v2"])
        for key, result in grouped_results:
            _, month = key
            periods.setdefault(key, {"month": month})
            periods[key]["billed_revenue"] = sum_item_amounts(result, [
                "0200", "0300", "0400", "0500", "0600", "1000", "1200",
            ])
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "collected_revenue", "billed_revenue",
        ])
        # Group periods by quarter and select latest month
        quarters = group_quarters(periods, sum_all_months)
        # Filter out quarters with no data
        quarters = filter(lambda o: o[1] != None, quarters)
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
