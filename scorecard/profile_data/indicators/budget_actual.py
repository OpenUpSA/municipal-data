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


def make_year_phase_group_key(group_lookup):
    def year_phase_group_key(d):
        return (
            d["financial_year_end.year"],
            d["amount_type.code"],
            group_lookup[d["item.code"]],
        )

    return year_phase_group_key


class TimeSeriesCalculator(IndicatorCalculator):
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        # budget_year - 1 temporarily because IBY1 and 2 are not available for budget year
        # at the moment with the mSCOA transition
        reducer = make_time_series_reducer(api_data.budget_year - 1)
        items = reduce(reducer, api_data.results[cls.api_data_key], [])
        return items


class IncomeTimeSeries(TimeSeriesCalculator):
    name = "income_time_series"
    api_data_key = "revenue_annual_totals"


class SpendingTimeSeries(TimeSeriesCalculator):
    name = "spending_time_series"
    api_data_key = "expenditure_annual_totals"


class AdjustmentsCalculator(IndicatorCalculator):
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        group_key = make_year_phase_group_key(cls.group_lookup)
        grouped = group_by(api_data.results[cls.api_data_key], group_key)
        year_phase_group = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: 0))
        )
        year_group = defaultdict(lambda: set())
        # sum up items in a group and track distinct group labels in each year
        for (year, phase, group_label), items in grouped.items():
            year_phase_group[year][phase][group_label] = sum(
                i["amount.sum"] for i in items
            )
            year_group[year].add(group_label)

        results = dict()
        for year in year_group.keys():
            results[year] = []
            for group_label in year_group[year]:
                budget = year_phase_group[year]["ORGB"][group_label]
                adjusted = year_phase_group[year]["ADJB"][group_label]
                results[year].append(
                    {
                        "item": group_label,
                        "comparison": "Original to adjusted budget",
                        "amount": adjusted - budget,
                        "percent_changed": percent(adjusted - budget, budget)
                        if budget
                        else None,
                    }
                )
                audited = year_phase_group[year]["AUDA"][group_label]
                results[year].append(
                    {
                        "item": group_label,
                        "comparison": "Original budget to audited outcome",
                        "amount": audited - budget,
                        "percent_changed": percent(audited - budget, budget)
                        if budget
                        else None,
                    }
                )
        return results


class IncomeAdjustments(AdjustmentsCalculator):
    name = "income_adjustments"
    api_data_key = "revenue_budget_actual"
    groups = [
        ("Property rates", ["0200", "0300"]),
        ("Service Charges", ["0400"]),
        ("Rental income", ["0700"]),
        ("Interest and investments", ["0800", "1000", "1100"]),
        ("Fines", ["1300"]),
        ("Licenses and Permits", ["1400"]),
        ("Other", ["1700", "1800", "1500"]),
        ("Government Transfers", ["1600", "1610"]),
    ]
    group_lookup = dict()
    for label, codes in groups:
        for code in codes:
            group_lookup[code] = label


class SpendingAdjustments(AdjustmentsCalculator):
    name = "spending_adjustments"
    api_data_key = "expenditure_budget_actual"
    groups = [
        ("Employee related costs", ["3000", "3100", "3200", "3300"]),
        ("Remuneration of councillors", ["3400"]),
        ("Finance charges", ["3600", "3900", "4000"]),
        ("Bulk purchases", ["4100"]),
        ("Contracted services", ["4200"]),
        ("Transfers and subsidies", ["4300"]),
        (
            "Other",
            [
                "3500",
                "3700",
                "4110",
                "4400",
                "4500",
                "4550",
            ],
        ),
    ]
    group_lookup = dict()
    for label, codes in groups:
        for code in codes:
            group_lookup[code] = label
