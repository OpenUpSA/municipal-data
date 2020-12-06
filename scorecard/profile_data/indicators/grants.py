from .indicator_calculator import IndicatorCalculator

class Grants(IndicatorCalculator):
    name = "grants"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = [d for d in api_data.results["grants_v1"] if d["amount.sum"] != 0]
        return {
            "values": values,
        }
