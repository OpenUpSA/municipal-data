from .utils import (
    ratio,
    group_items_by_year,
    sum_item_amounts,
    filter_for_all_keys,
)
from .indicator_calculator import IndicatorCalculator


class LiquidityRatio(IndicatorCalculator):
    """
    The municipality's immediate ability to pay its current liabilities.
    """

    name = "liquidity_ratio"
    result_type = "ratio"
    noun = "ratio"
    has_comparisons = True

    @classmethod
    def determine_rating(cls, result):
        return "good" if result >= 1 else "bad"

    @classmethod
    def generate_data(cls, year, values):
        data = {
            "date": "%s" % (year),
            "year": year,
        }
        if values:
            cash = values["cash"]
            call_investment_deposits = values["call_investment_deposits"]
            total_current_liabilities = values["total_current_liabilities"]
            result = ratio(
                cash + call_investment_deposits, total_current_liabilities
            )
            data.update({
                "amount_type": "ACT",
                "cash": cash,
                "call_investment_deposits": call_investment_deposits,
                "liabilities": total_current_liabilities,
                "result": result,
                "rating": cls.determine_rating(result),
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
        grouped_results = group_items_by_year(results["bsheet_auda_years"])
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["cash"] = result.get("1800")
            periods[key]["call_investment_deposits"] = result.get("2200")
            periods[key]["total_current_liabilities"] = result.get("1600")
        # Populate periods with v2 data
        grouped_results = group_items_by_year(results["bsheet_auda_years_v2"])
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["cash"] = result.get("0120")
            periods[key]["call_investment_deposits"] = result.get("0130")
            periods[key]["total_current_liabilities"] = sum_item_amounts(result, [
                "0330", "0340", "0350", "0360", "0370",
            ])
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "cash",
            "call_investment_deposits",
            "total_current_liabilities",
        ])
        # Convert periods into dictionary
        periods = dict(periods)
        # Generate data for the reuqested years
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
            "ref": api_data.references["mbrr"],
        }
