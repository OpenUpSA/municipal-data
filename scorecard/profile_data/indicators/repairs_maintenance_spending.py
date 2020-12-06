from .indicator_calculator import IndicatorCalculator
from .utils import (
    percent,
    populate_periods,
    group_by_year,
    filter_for_all_keys,
)


class RepairsMaintenanceSpending(IndicatorCalculator):
    """
    Spending on Repairs and Maintenance as a percentage of Property, Plant and
    Equipment.
    """

    name = "repairs_maintenance_spending"
    result_type = "%"
    noun = "spending"
    has_comparisons = True

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
            })
        else:
            data.update({
                "result": None,
                "rating": None,
            })
        return data

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
        periods = {}
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_by_year(
                results["repairs_maintenance_v1"],
                "repairs_maintenance",
            ),
            "repairs_maintenance",
        )
        populate_periods(
            periods,
            group_by_year(results["property_plant_equipment_v1"]),
            "property_plant_equipment",
        )
        populate_periods(
            periods,
            group_by_year(results["investment_property_v1"]),
            "investment_property",
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_by_year(results["repairs_maintenance_v2"]),
            "repairs_maintenance",
        )
        populate_periods(
            periods,
            group_by_year(results["property_plant_equipment_v2"]),
            "property_plant_equipment",
        )
        populate_periods(
            periods,
            group_by_year(results["investment_property_v2"]),
            "investment_property",
        )
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "repairs_maintenance",
            "property_plant_equipment",
            "investment_property",
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
