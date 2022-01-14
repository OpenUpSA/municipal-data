
from .series import SeriesIndicator
from .utils import (
    percent,
    group_by_year,
    populate_periods,
    filter_for_all_keys_versioned,
)


class OperatingBudgetSpending(SeriesIndicator):
    """
    Difference between budgeted operating expenditure and what was actually
    spent.
    """

    name = "operating_budget_spending"
    result_type = "%"
    noun = "underspending or overspending"
    has_comparisons = True
    reference = "overunder"
    formula = {
        "text": "= ((Actual Operating Expenditure - Budget Operating Expenditure) / Budgeted Operating Expenditure) * 100",
        "actual": [
            "=", 
            "(",
            "(",
            {
                "cube": "incexp",
                "item_codes": ["4600"],
                "amount_type": "AUDA",
            },
            "-",
            {
                "cube": "incexp",
                "item_codes": ["4600"],
                "amount_type": "ADJB",
            },
            ")",
            "/",
            {
                "cube": "incexp",
                "item_codes": ["4600"],
                "amount_type": "ADJB",
            },
            ")",
            "*",
            "100",
        ],
    }

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
                "cube_version": values["cube_version"],
            })
        else:
            data.update({
                "result": None,
                "rating": None,
                "overunder": None,
                "cube_version": None,
            })
        return data

    @classmethod
    def get_values(cls, years, results):
        periods = {}
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_actual_v1"]),
            ("operating_expenditure_actual","v1"),
        )
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_budget_v1"]),
            ("operating_expenditure_budget","v1"),
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_actual_v2"]),
            ("operating_expenditure_actual","v2"),
        )
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_budget_v2"]),
            ("operating_expenditure_budget","v2"),
        )
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys_versioned(periods, [
            "operating_expenditure_actual",
            "operating_expenditure_budget",
        ])
        # Convert periods into dictionary
        periods = dict(periods)
        # Generate data for the requested years
        return list(
            map(
                lambda year: cls.generate_data(year, periods.get(year)),
                years,
            )
        )
