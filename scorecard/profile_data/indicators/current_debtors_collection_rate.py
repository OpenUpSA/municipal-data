
from .series import SeriesIndicator
from .utils import (
    percent,
    group_items_by_year,
    filter_for_all_keys,
    sum_item_amounts,
    data_source_version,
)


class CurrentDebtorsCollectionRate(SeriesIndicator):
    """
    The percentage of new revenue (generated within the financial year) that a
    municipality actually collects.
    """

    name = "current_debtors_collection_rate"
    result_type = "%"
    noun = "rate"
    has_comparisons = True
    reference = "mbrr"
    formula = {
        "text": "= (Collected Revenue / Billed Revenue) * 100",
        "actual": [
            "=", 
            "(",
            {
                "cube": "cflow",
                "item_codes": [
                    "3010", "3030", "3040", "3050", "3060", "3070", "3100",
                ],
                "amount_type": "AUDA",
            },
            "/",
            {
                "cube": "incexp",
                "item_codes": [
                    "0200", "0400", "1000 less item code 2000",
                ],
                "amount_type": "AUDA",
            },
            ")",
            "*",
            "100",
        ],
    }
    formula_v2 = {
        "text": "= (Collected Revenue / Billed Revenue) * 100",
        "actual": [
            "=", 
            "(",
            {
                "cube": "cflow_v2",
                "item_codes": [
                    "0120", "0130", "0280",
                ],
                "amount_type": "AUDA",
            },
            "/",
            {
                "cube": "incexp_v2",
                "item_codes": [
                    "0200", "0300", "0400", "0500", "0600", "0800", "0900", "1000",
                ],
                "amount_type": "AUDA",
            },
            ")",
            "*",
            "100",
        ],
    }

    @classmethod
    def detemine_rating(cls, result):
        return "good" if round(result) >= 95 else "bad"

    @classmethod
    def generate_data(cls, year, values):
        data = {
            "year": year,
            "date": "%s" % (year),
        }
        if values:
            collected_revenue = values["collected_revenue"]
            billed_revenue = values["billed_revenue"]
            result = percent(collected_revenue, billed_revenue)
            data.update({
                "amount_type": "AUDA",
                "result": result,
                "rating": cls.detemine_rating(result),
                "cube_version": data_source_version(year),
            })
        else:
            data.update({
                "result": None,
                "rating": "bad",
                "receipts": None,
                "billing": None,
                "cube_version": None,
            })
        return data

    @classmethod
    def get_values(cls, years, results):
        periods = {}
        # Populate periods with v1 cash flow data
        grouped_results = group_items_by_year(results["cflow_auda_years"])
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["collected_revenue"] = sum_item_amounts(result, [
                "3010", "3030", "3040", "3050", "3060", "3070", "3100",
            ])
        # Populate periods with v1 income and expenditure data
        grouped_results = group_items_by_year(results["incexp_auda_years"])
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["billed_revenue"] = sum_item_amounts(result, [
                "0200", "0400", "1000",
            ]) - result.get("2000", 0)
        # Populate periods with v2 cash flow data
        grouped_results = group_items_by_year(results["cflow_auda_years_v2"])
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["collected_revenue"] = sum_item_amounts(result, [
                "0120", "0130", "0280",
            ])
        # Populate periods with v2 income and expenditure data
        grouped_results = group_items_by_year(results["incexp_auda_years_v2"])
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["billed_revenue"] = sum_item_amounts(result, [
                "0200", "0300", "0400", "0500", "0600", "0800", "0900", "1000",
            ])
        # Filter out periods that don't have all the required data
        # print(periods)
        periods = filter_for_all_keys(periods, [
            "collected_revenue", "billed_revenue",
        ])
        # Convert the periods to a dictionary
        periods = dict(periods)
        # Compile the data for the expected quarters, starting with the latest
        return list(
            map(
                lambda year: cls.generate_data(year, periods.get(year)),
                years,
            )
        )
