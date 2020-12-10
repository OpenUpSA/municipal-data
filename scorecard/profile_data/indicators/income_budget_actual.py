from .indicator_calculator import IndicatorCalculator
from itertools import groupby
from .utils import year_key
from functools import reduce
import re
from collections import defaultdict

GROUPS = [
    ("Property rates", ["0200", "0300"]),
    ("Service Charges", ["0400"]),
    ("Rental income", ["0700"]),
    ("Interest and investments", ["0800", "1000", "1100"]),
    ("Fines", ["1300"]),
    ("Licenses and Permits", ["1400"]),
    ("Agency services", ["1500"]),
    ("Other", ["1700", "1800"]),
    ("Government Transfers for Operating Expenses", ["1600"]),
    ("Government Transfers for Capital Expenses", ["1610"]),
]


def make_time_series_reducer(budget_year):
    def time_series_reducer(accumulator, current_value):
        reporting_year = current_value["financial_year_end.year"]
        budget_phase = current_value["amount_type.code"]

        # Drop all forecast except those reported in budget_year
        if budget_phase in {"IBY1", "IBY2"} and reporting_year != budget_year:
            return accumulator

        if budget_phase == "IBY1":
            current_value["financial_year"] = reporting_year + 1
        elif budget_phase == "IBY2":
            current_value["financial_year"] = reporting_year + 2
        else:
            current_value["financial_year"] = reporting_year
        delete current_value["financial_year_end.year"]
        current_value["budget_phase"] = current_value.pop("amount_type.label")
        current_value["amount"] = current_value.pop("amount.sum")

        return [*accumulator, current_value]
    return time_series_reducer


class IncomeTimeSeries(IndicatorCalculator):
    name = "income_time_series"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        reducer = make_time_series_reducer(api_data.budget_year-1)
        items = reduce(reducer, api_data.results["revenue_annual_totals"], [])
        return items
