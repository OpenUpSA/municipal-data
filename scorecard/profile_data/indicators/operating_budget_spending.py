
from .utils import (
    percent,
    group_by_year,
    populate_periods,
    filter_for_all_keys,
)
from .indicator_calculator import IndicatorCalculator


def translate_rating(result):
    if abs(result) <= 5:
        return "good"
    elif abs(result) <= 15:
        return "ave"
    elif abs(result) > 15:
        return "bad"
    else:
        return None


def generate_data(year, values):
    data = {
        "date": year,
    }
    if values:
        actual = values["operating_expenditure_actual"]
        budget = values["operating_expenditure_budget"]
        diffirence = actual - budget
        result = percent(diffirence, budget, 1)
        data.update({
            "result": result,
            "rating": translate_rating(result),
            "overunder": "under" if result < 0 else "over",
        })
    else:
        data.update({
            "result": None,
            "rating": None,
            "overunder": None,
        })
    return data


class OperatingBudgetSpending(IndicatorCalculator):
    indicator_name = "operating_budget_spending"
    result_type = "%"
    noun = "underspending or overspending"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
        periods = {}
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_actual_v1"]),
            "operating_expenditure_actual",
        )
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_budget_v1"]),
            "operating_expenditure_budget",
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_actual_v2"]),
            "operating_expenditure_actual",
        )
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_budget_v2"]),
            "operating_expenditure_budget",
        )
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "operating_expenditure_actual",
            "operating_expenditure_budget",
        ])
        # Convert periods into dictionary
        periods = dict(periods)
        # Generate data for the requested years
        values = list(
            map(
                lambda year: generate_data(year, periods.get(year)),
                api_data.years,
            )
        )
        # Return the compiled data
        return {
            "values": values,
            "ref": api_data.references["overunder"],
        }
