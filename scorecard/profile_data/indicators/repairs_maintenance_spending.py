
from .series import SeriesIndicator
from .utils import (
    percent,
    populate_periods,
    group_by_year,
    filter_for_all_keys_versioned,
    data_source_version,
)


class RepairsMaintenanceSpending(SeriesIndicator):
    """
    Spending on Repairs and Maintenance as a percentage of Property, Plant and
    Equipment.
    """

    name = "repairs_maintenance_spending"
    result_type = "%"
    noun = "spending"
    has_comparisons = True
    reference = "circular71"
    formula = {
        "text": "= (Repairs and maintenance expenditure / (Property, Plant and Equipment + Investment Property)) * 100",
        "actual": [
            "=", 
            "(",
            {
                "cube": "capital",
                "item_codes": ["4100"],
                "amount_type": "AUDA",
            },
            "/",
            "(",
            {
                "cube": "bsheet",
                "item_codes": ["1300"],
                "amount_type": "AUDA",
            },
            "+",
            {
                "cube": "bsheet",
                "item_codes": ["1401"],
                "amount_type": "AUDA",
            },
            ")",
            ")",
            "*",
            "100",
        ],
    }
    formula_v2 = {
        "text": "= (Repairs and maintenance expenditure / (Property, Plant and Equipment + Investment Property)) * 100",
        "actual": [
            "=", 
            "(",
            {
                "cube": "capital_v2",
                "item_description": "Total",
                "amount_type": "AUDA",
            },
            "/",
            "(",
            {
                "cube": "financial_position_v2",
                "item_codes": ["0240"],
                "amount_type": "AUDA",
            },
            "+",
            {
                "cube": "financial_position_v2",
                "item_codes": ["0220"],
                "amount_type": "AUDA",
            },
            ")",
            ")",
            "*",
            "100",
        ],
    }

    @classmethod
    def determine_rating(cls, result):
        if abs(result) >= 8:
            return "good"
        elif abs(result) < 8:
            return "bad"
        else:
            return None

    @classmethod
    def generate_data(cls, year, values):
        data = {
            "date": year,
        }
        if values:
            repairs_maintenance = values["repairs_maintenance"]
            property_plant_equipment = values["property_plant_equipment"]
            investment_property = values["investment_property"]
            result = percent(
                repairs_maintenance,
                (property_plant_equipment + investment_property),
            )
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
            group_by_year(
                results["repairs_maintenance_v1"],
                "repairs_maintenance",
            ),
            ("repairs_maintenance", "v1"),
        )
        populate_periods(
            periods,
            group_by_year(results["property_plant_equipment_v1"]),
            ("property_plant_equipment", "v1"),
        )
        populate_periods(
            periods,
            group_by_year(results["investment_property_v1"]),
            ("investment_property", "v1"),
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_by_year(results["repairs_maintenance_v2"]),
            ("repairs_maintenance", "v2"),
        )
        populate_periods(
            periods,
            group_by_year(results["property_plant_equipment_v2"]),
            ("property_plant_equipment", "v2"),
        )
        populate_periods(
            periods,
            group_by_year(results["investment_property_v2"]),
            ("investment_property", "v2"),
        )
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys_versioned(periods, [
            "repairs_maintenance",
            "property_plant_equipment",
            "investment_property",
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
