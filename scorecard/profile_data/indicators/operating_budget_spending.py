
from .utils import (
    percent,
    group_by_year,
    populate_periods,
    filter_for_all_keys,
)
from .indicator_calculator import IndicatorCalculator


class OperatingBudgetSpending(IndicatorCalculator):
    indicator_name = "operating_budget_spending"
    result_type = "%"
    noun = "underspending or overspending"
    has_comparisons = True

    @classmethod
    def determine_rating(cls, result):
        if abs(result) <= 5:
            return "good"
        elif abs(result) <= 15:
            return "ave"
        elif abs(result) > 15:
            return "bad"
        else:
            return None

    @classmethod
    def generate_data(cls, year, values):
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
                "rating": cls.determine_rating(result),
                "overunder": "under" if result < 0 else "over",
            })
        else:
            data.update({
                "result": None,
                "rating": None,
                "overunder": None,
            })
        return data

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
                lambda year: cls.generate_data(year, periods.get(year)),
                api_data.years,
            )
        )
        # Return the compiled data
        return {
            "result_type": cls.result_type,
            "values": values,
            "ref": api_data.references["overunder"],
        }
