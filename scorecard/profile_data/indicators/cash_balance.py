from .series import SeriesIndicator
from .utils import (
    group_by_year,
    populate_periods,
    filter_for_all_keys_versioned,
)


class CashBalance(SeriesIndicator):
    """
    Cash balance at the end of the financial year.
    """

    name = "cash_balance"
    result_type = "R"
    noun = "cash balance"
    has_comparisons = True
    reference = "solgf"
    formula = {
        "text": "= Cash available at year end",
        "actual": [
            "=", 
            {
                "cube": "cflow",
                "item_codes": ["4200"],
                "amount_type": "AUDA",
            }
        ],
    }

    @classmethod
    def determine_rating(cls, result):
        if result > 0:
            return "good"
        elif result <= 0:
            return "bad"
        else:
            return None

    @classmethod
    def generate_data(cls, year, values):
        data = {
            "date": year,
        }
        if values:
            cash_at_year_end = values["cash_at_year_end"]
            data.update({
                "result": cash_at_year_end,
                "rating": cls.determine_rating(cash_at_year_end),
                "cube_version": values["cube_version"],
            })
        else:
            data.update({
                "result": None,
                "rating": "bad",
                "cube_version": None,
            })
        return data

    @classmethod
    def get_values(cls, years, results):
        periods = {}
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_by_year(results["cash_flow_v1"]),
            ("cash_at_year_end","v1"),
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_by_year(results["cash_flow_v2"]),
            ("cash_at_year_end","v2"),
        )
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys_versioned(periods, [
            "cash_at_year_end",
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

