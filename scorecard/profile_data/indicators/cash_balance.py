
from .indicator_calculator import IndicatorCalculator
from .utils import (
    group_by_year,
    populate_periods,
)


class CashBalance(IndicatorCalculator):
    indicator_name = "cash_balance"
    result_type = "R"
    noun = "cash balance"
    has_comparisons = True

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
            })
        else:
            data.update({
                "result": None,
                "rating": "bad",
            })
        return data

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
        periods = {}
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_by_year(results["cash_flow_v1"]),
            "cash_at_year_end",
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_by_year(results["cash_flow_v2"]),
            "cash_at_year_end",
        )
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
            "ref": api_data.references["solgf"],
        }
