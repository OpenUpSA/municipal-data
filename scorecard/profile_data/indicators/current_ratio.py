
from .series import SeriesIndicator
from .utils import (
    ratio,
    sum_item_amounts,
    filter_for_all_keys,
    group_items_by_year,
    data_source_version,
)


class CurrentRatio(SeriesIndicator):
    """
    The value of a municipality's short-term assets as a multiple of its
    short-term liabilities.
    """

    name = "current_ratio"
    result_type = "ratio"
    noun = "ratio"
    has_comparisons = True
    reference = "circular71"
    formula = {
        "text": "= Current Assets / Current Liabilities",
        "actual": [
            "=", 
            {
                "cube": "bsheet",
                "item_codes": ["2150"],
                "amount_type": "AUDA",
            },
            "/",
            {
                "cube": "bsheet",
                "item_codes": ["1600"],
                "amount_type": "AUDA",
            },
        ],
    }
    formula_v2 = {
        "text": "= Current Assets / Current Liabilities",
        "actual": [
            "=", 
            {
                "cube": "bsheet_v2",
                "item_codes": ["2150"],
                "amount_type": "AUDA",
            },
            "/",
            {
                "cube": "bsheet_v2",
                "item_codes": ["1600"],
                "amount_type": "AUDA",
            },
        ],
    }

    @classmethod
    def determine_rating(cls, value):
        if value >= 1.5:
            return "good"
        elif value >= 1:
            return "ave"
        else:
            return "bad"

    @classmethod
    def generate_data(cls, year, values):
        data = {
            "date": year,
            "year": year,
        }
        if values:
            assets = values["assets"]
            liabilities = values["liabilities"]
            result = ratio(assets, liabilities)
            data.update({
                "amount_type": "AUDA",
                "assets": assets,
                "liabilities": liabilities,
                "result": result,
                "rating": cls.determine_rating(result),
                "cube_version": data_source_version(year),
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
        grouped_results = group_items_by_year(results["bsheet_auda_years"])
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["assets"] = result.get("2150")
            periods[key]["liabilities"] = result.get("1600")
        # Populate periods with v2 data
        grouped_results = group_items_by_year(
            results["financial_position_auda_years_v2"]
        )
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["assets"] = sum_item_amounts(result, [
                "0120", "0130", "0140", "0150", "0160", "0170",
            ])
            periods[key]["liabilities"] = sum_item_amounts(result, [
                "0330", "0340", "0350", "0360", "0370",
            ])
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "assets", "liabilities",
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
