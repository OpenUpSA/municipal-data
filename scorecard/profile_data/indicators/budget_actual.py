from .indicator_calculator import IndicatorCalculator
from .utils import group_by, percent
from functools import reduce
from collections import defaultdict


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
        del current_value["financial_year_end.year"]
        current_value["budget_phase"] = current_value.pop("amount_type.label")
        current_value["amount"] = current_value.pop("amount.sum")

        return [*accumulator, current_value]

    return time_series_reducer


def combine_versions(v1, v2):
    key =  lambda item: (item["financial_year_end.year"], item["amount_type.code"])
    unique_year_phases = set()
    for item in v2:
        unique_year_phases.add(key(item))

    def filter_function(item):
        return key(item) not in unique_year_phases

    return [*filter(filter_function, v1), *v2]


class TimeSeriesCalculator(IndicatorCalculator):
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        reducer = make_time_series_reducer(api_data.budget_year)
        combined_data = combine_versions(
            api_data.results[cls.v1_api_data_key],
            api_data.results[cls.v2_api_data_key]
        )
        items = reduce(reducer, combined_data, [])
        return items


class IncomeTimeSeries(TimeSeriesCalculator):
    name = "income_time_series"
    v1_api_data_key = "revenue_annual_totals_v1"
    v2_api_data_key = "revenue_annual_totals_v2"


class SpendingTimeSeries(TimeSeriesCalculator):
    name = "spending_time_series"
    v1_api_data_key = "expenditure_annual_totals_v1"
    v2_api_data_key = "expenditure_annual_totals_v2"


def none_subtract(a, b):
    if a is None:
        return None
    if b is None:
        return None
    return a - b


def none_percent(numerator, denominator):
    if numerator is None:
        return None
    if denominator is None:
        return None
    return percent(numerator, denominator)


def make_year_group_phase_key(group_lookup):
    def year_phase_group_key(d):
        return (
            d["financial_year_end.year"],
            group_lookup[d["item.code"]],
            d["amount_type.code"],
        )
    return year_phase_group_key


class AdjustmentsCalculator(IndicatorCalculator):
    """
    For each year with at least some data, we should emit adjustment items for those items.
    If ORGB is missing, all adjustments will be None - unknown.
    If ADJB or ADUA is missing, those adjustments will be None - unknown.
    """
    has_comparisons = False

    @classmethod
    def group_sum_items(cls, api_data):
        v1_group_key = make_year_group_phase_key(cls.v1_group_lookup)
        v2_group_key = make_year_group_phase_key(cls.v2_group_lookup)
        v1_grouped = group_by(api_data.results[cls.v1_api_data_key], v1_group_key)
        v2_grouped = group_by(api_data.results[cls.v2_api_data_key], v2_group_key)

        # Defaultdict to treat missing values as zero
        v1_year_grouplabel_phase = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: None))
        )
        v2_year_grouplabel_phase = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: None))
        )

        # sum up items in a group
        for (year, group_label, phase), items in v1_grouped.items():
            v1_year_grouplabel_phase[year][group_label][phase] = sum(
                i["amount.sum"] for i in items
            )
        for (year, group_label, phase), items in v2_grouped.items():
            v2_year_grouplabel_phase[year][group_label][phase] = sum(
                i["amount.sum"] for i in items
            )

        # Combine v1 and v2 data.
        # Prefer entire year in v2 over that year in v1.
        year_grouplabel_phase = v1_year_grouplabel_phase.copy()
        year_grouplabel_phase.update(v2_year_grouplabel_phase)
        return year_grouplabel_phase

    @classmethod
    def calculate_adjustments(cls, year_grouplabel_phase_sum):
        results = dict()
        for year, grouplabel_phase in year_grouplabel_phase_sum.items():
            results[year] = []
            for group_label in grouplabel_phase.keys():
                budget = year_grouplabel_phase_sum[year][group_label]["ORGB"]
                adjusted = year_grouplabel_phase_sum[year][group_label]["ADJB"]
                adjusted_change = none_subtract(adjusted, budget)
                results[year].append({
                    "item": group_label,
                    "comparison": "Original to adjusted budget",
                    "amount": adjusted_change,
                    "percent_changed": none_percent(adjusted_change, budget),
                })
                audited = year_grouplabel_phase_sum[year][group_label]["AUDA"]
                audited_change = none_subtract(audited, budget)
                results[year].append({
                    "item": group_label,
                    "comparison": "Original budget to audited outcome",
                    "amount": audited_change,
                    "percent_changed": none_percent(audited_change, budget),
                })
        return results

    @classmethod
    def get_muni_specifics(cls, api_data):
        year_grouplabel_phase_sum = cls.group_sum_items(api_data)
        results = cls.calculate_adjustments(year_grouplabel_phase_sum)
        for list_ in results.values():
            list_.sort(key=lambda x: x["item"])
        return results


class IncomeAdjustments(AdjustmentsCalculator):
    name = "income_adjustments"
    v1_api_data_key = "revenue_budget_actual_v1"
    v2_api_data_key = "revenue_budget_actual_v2"
    v1_group_lookup = {
        "0200": "Property rates",
        "0300": "Property rates",
        "0400": "Service Charges",
        "0700": "Rental income",
        "0800": "Interest and investments",
        "1000": "Interest and investments",
        "1100": "Interest and investments",
        "1300": "Fines",
        "1400": "Licenses and Permits",
        "1700": "Other",
        "1800": "Other",
        "1500": "Other",
        "1600": "Government Transfers",
        "1610": "Government Transfers",
    }
    v2_group_lookup = {
        "0200": "Property rates",
        "0300": "Service Charges",
        "0400": "Service Charges",
        "0500": "Service Charges",
        "0600": "Service Charges",
        "0800": "Rental income",
        "0900": "Interest and investments",
        "1000": "Interest and investments",
        "1100": "Interest and investments",
        "1200": "Fines",
        "1300": "Licenses and Permits",
        "1400": "Other",
        "1600": "Other",
        "1700": "Other",
        "1500": "Government Transfers",
    }


class SpendingAdjustments(AdjustmentsCalculator):
    name = "spending_adjustments"
    v1_api_data_key = "expenditure_budget_actual_v1"
    v2_api_data_key = "expenditure_budget_actual_v2"
    v1_group_lookup = {
        "3000": "Employee related costs",
        "3100": "Employee related costs",
        "3200": "Employee related costs",
        "3300": "Employee related costs",
        "3400": "Remuneration of councillors",
        "3600": "Finance charges",
        "3900": "Finance charges",
        "4000": "Finance charges",
        "4100": "Bulk purchases",
        "4200": "Contracted services",
        "4300": "Transfers and subsidies",
        "3500": "Other",
        "3700": "Other",
        "4110": "Other",
        "4400": "Other",
        "4500": "Other",
        "4550": "Other",
    }
    v2_group_lookup = {
        "2000": "Employee related costs",
        "2100": "Remuneration of councillors",
        "2400": "Finance charges",
        "2500": "Bulk purchases",
        "2700": "Contracted services",
        "2800": "Transfers and subsidies",
        "2200": "Other",
        "2300": "Other",
        "2600": "Other",
        "2900": "Other",
        "3000": "Other",
    }
