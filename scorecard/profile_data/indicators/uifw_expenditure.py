from .indicator_calculator import IndicatorCalculator
from .utils import (
    percent,
    group_by_year,
    populate_periods,
    filter_for_all_keys,
)


class UIFWExpenditure(IndicatorCalculator):
    name = "uifw_expenditure"
    result_type = "%"
    noun = "expenditure"
    has_comparisons = True

    @classmethod
    def determine_rating(cls, result):
        if result == 0:
            return "good"
        else:
            return "bad"

    @classmethod
    def generate_data(cls, year, values):
        result = None
        rating = None
        if values:
            uifw_expenditure = values["uifw_expenditure"]
            operating_expenditure = values["operating_expenditure"]
            result = percent(uifw_expenditure, operating_expenditure)
            rating = cls.determine_rating(result)
        return {
            "date": year,
            "result": result,
            "rating": rating,
        }

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
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
            "ref": api_data.references["circular71"],
        }
