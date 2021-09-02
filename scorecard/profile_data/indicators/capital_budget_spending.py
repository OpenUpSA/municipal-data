
from .series import SeriesIndicator
from .utils import (
    group_by_year,
    populate_periods,
    filter_for_all_keys,
    percent,
)


class CapitalBudgetSpending(SeriesIndicator):
    """
    Difference between budgeted capital expenditure and what was actually
    spent.
    """

    name = "capital_budget_spending"
    result_type = "%"
    noun = "underspending or overspending"
    has_comparisons = True
    reference = "overunder"
    formula = {
        "text": "= ((Actual Capital Expenditure - Budgeted Capital Expenditure) / Budgeted Capital Expenditure) * 100",
        "actual": [
            "=",
            "(",
            "(",
            {
                "cube": "capital",
                "item_codes": ["4100"],
                "amount_type": "AUDA",
            },
            "-",
            {
                "cube": "capital",
                "item_codes": ["4100"],
                "amount_type": "ADJB",
            },
            ")",
            "/",
            {
                "cube": "capital",
                "item_codes": ["4100"],
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
            budget = values["budget"]
            actual = values["actual"]
            result = percent((actual - budget), budget)
            data.update({
                "result": result,
                "overunder": "under" if result < 0 else "over",
                "rating": cls.determine_rating(result),
            })
        else:
            data.update({
                "result": None,
                "overunder": None,
                "rating": None,
            })
        return data

    @classmethod
    def get_values(cls, years, results):
        periods = {}
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_by_year(
                results["capital_expenditure_budget_v1"],
                "total_assets",
            ),
            "budget",
        )
        populate_periods(
            periods,
            group_by_year(
                results["capital_expenditure_actual_v1"],
                "total_assets",
            ),
            "actual",
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_by_year(results["capital_expenditure_budget_v2"]),
            "budget",
        )
        populate_periods(
            periods,
            group_by_year(results["capital_expenditure_actual_v2"]),
            "actual",
        )
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "budget", "actual",
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
