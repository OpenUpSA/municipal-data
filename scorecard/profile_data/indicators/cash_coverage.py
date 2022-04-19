
from .series import SeriesIndicator
from .utils import (
    ratio,
    group_by_year,
    filter_for_all_keys,
    populate_periods,
    data_source_version,
)


class CashCoverage(SeriesIndicator):
    """
    Months of operating expenses can be paid for with the cash available.
    """

    name = "cash_coverage"
    result_type = "months"
    noun = "coverage"
    has_comparisons = True
    reference = "solgf"
    formula = {
        "text": "= Cash available at year end / Operating Expenditure per month",
        "actual": [
            "=", 
            {
                "cube": "cflow",
                "item_codes": ["4200"],
                "amount_type": "AUDA",
            },
            "/",
            "(",
            {
                "cube": "incexp",
                "item_codes": ["4600"],
                "amount_type": "AUDA",
            },
            "/",
            "12",
            ")",
        ],
    }
    formula_v2 = {
        "text": "= Cash available at year end / Operating Expenditure per month",
        "actual": [
            "=", 
            {
                "cube": "cflow_v2",
                "item_codes": ["0430"],
                "amount_type": "AUDA",
            },
            "/",
            "(",
            {
                "cube": "incexp_v2",
                "item_codes": ["2000", "2100", "2200", "2300", "2400", "2500", "2600", "2700", "2800", "2900", "3000"],
                "amount_type": "AUDA",
            },
            "/",
            "12",
            ")",
        ],
    }

    @classmethod
    def determine_rating(cls, result):
        if result > 3:
            return "good"
        elif result <= 1:
            return "bad"
        else:
            return "ave"

    @classmethod
    def generate_data(cls, year, values):
        data = {
            "date": year,
        }
        if values:
            cash_at_year_end = values["cash_at_year_end"]
            monthly_expenses = values["operating_expenditure"] / 12
            calculated_ratio = ratio(cash_at_year_end, monthly_expenses, 1)
            result = max(calculated_ratio, 0)
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
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_by_year(results["cash_flow_v1"]),
            "cash_at_year_end",
        )
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_actual_v1"]),
            "operating_expenditure",
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_by_year(results["cash_flow_v2"]),
            "cash_at_year_end",
        )
        populate_periods(
            periods,
            group_by_year(results["operating_expenditure_actual_v2"]),
            "operating_expenditure",
        )
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "cash_at_year_end", "operating_expenditure",
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
