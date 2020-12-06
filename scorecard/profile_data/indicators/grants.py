from .indicator_calculator import IndicatorCalculator
from itertools import groupby
from .utils import year_key
from constance import config


class Grants(IndicatorCalculator):
    name = "grants"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = [d for d in api_data.results["grants_v1"] if d["amount.sum"] != 0]
        grouped_values = groupby(sorted(values, key=year_key), key=year_key)
        dictionary = dict(map(lambda g: (g[0], list(g[1])), grouped_values))
        return {
            "values": dictionary,
            "snapshot_date": {
                "year": config.GRANTS_LATEST_YEAR,
                "quarter": config.GRANTS_LATEST_QUARTER,
            },
        }
