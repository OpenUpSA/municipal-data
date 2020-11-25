
from .indicator_calculator import IndicatorCalculator
from .utils import (
    group_amount_by_year,
    populate_periods,
)


def translate_rating(result):
    if result > 0:
        return "good"
    elif result <= 0:
        return "bad"
    else:
        return None


def generate_data(year, values):
    data = {
        "date": year,
    }
    if values:
        cash_at_year_end = values["cash_at_year_end"]
        data.update({
            "result": cash_at_year_end,
            "rating": translate_rating(cash_at_year_end),
        })
    else:
        data.update({
            "result": None,
            "rating": "bad",
        })
    return data


class CashBalance(IndicatorCalculator):
    indicator_name = "cash_balance"
    result_type = "R"
    noun = "cash balance"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
        periods = {}
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_amount_by_year(results["cash_flow_v1"]),
            "cash_at_year_end",
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_amount_by_year(results["cash_flow_v2"]),
            "cash_at_year_end",
        )
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
            "ref": api_data.references["solgf"],
        }
