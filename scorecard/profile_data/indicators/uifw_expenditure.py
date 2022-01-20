
from .series import SeriesIndicator
from .utils import (
    percent,
    group_by_year,
    populate_periods,
    filter_for_all_keys,
    data_source_version,
)


class UIFWExpenditure(SeriesIndicator):
    """
    Unauthorised, Irregular, Fruitless and Wasteful Expenditure as a percentage
    of operating expenditure.
    """

    name = "uifw_expenditure"
    result_type = "%"
    noun = "expenditure"
    has_comparisons = True
    reference = "circular71"
    formula = {
        "text": "= (Unauthorised, Irregular, Fruitless and Wasteful Expenditure / Actual Operating Expenditure) * 100",
        "actual": [
            "=",
            "(",
            {
                "cube": "uifwexp",
                "item_codes": ["irregular", "fruitless", "unauthorised"],
            },
            "/",
            {
                "cube": "incexp",
                "item_codes": ["4600"],
                "amount_type": "AUDA",
            },
            ")",
            "*",
            "100",
        ],
    }
    formula_v2 = {
        "text": "= (Unauthorised, Irregular, Fruitless and Wasteful Expenditure / Actual Operating Expenditure) * 100",
        "actual": [
            "=",
            "(",
            {
                "cube": "uifwexp_v2",
                "item_codes": ["irregular", "fruitless", "unauthorised"],
            },
            "/",
            {
                "cube": "incexp_v2",
                "item_codes": ["4600"],
                "amount_type": "AUDA",
            },
            ")",
            "*",
            "100",
        ],
    }

    @classmethod
    def determine_rating(cls, result):
        if result == 0:
            return "good"
        else:
            return "bad"

    @classmethod
    def generate_data(cls, year, values):
        data = {
            "date": year,
        }
        if values:
            uifw_expenditure = values["uifw_expenditure"]
            operating_expenditure = values["operating_expenditure"]
            result = percent(uifw_expenditure, operating_expenditure)

            data.update({
                "result": result,
                "rating": cls.determine_rating(result),
                "cube_version": data_source_version(year),
            })
        else:
            data.update({
                "result": None,
                "rating": None,
                "cube_version": None,
            })
        return data

    @classmethod
    def get_values(cls, years, results):
        periods = {}
        # Populate periods with UIFW expenditure data
        populate_periods(
            periods,
            group_by_year(results["uifw_expenditure"]),
            "uifw_expenditure",
        )
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_actual_v1"]),
            "operating_expenditure",
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_actual_v2"]),
            "operating_expenditure",
        )
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "uifw_expenditure", "operating_expenditure",
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
