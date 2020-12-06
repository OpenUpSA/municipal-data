from .indicator_calculator import IndicatorCalculator
from itertools import groupby
from .utils import year_key
from constance import config
from functools import reduce
import re


PROVINCIAL_CODE = re.compile("^00\d\d$")


class Grants(IndicatorCalculator):
    name = "grants"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = cls.exclude_zeros(api_data.results["grants_v1"])
        national_grants, provincial_transfers = cls.split_nat_prov(values)
        nat_year_groups = groupby(sorted(national_grants, key=year_key), key=year_key)
        prov_year_groups = groupby(sorted(provincial_transfers, key=year_key), key=year_key)
        nat_years_dictionary = dict(map(lambda g: (g[0], list(g[1])), nat_year_groups))
        prov_years_dictionary = dict(map(lambda g: (g[0], list(g[1])), prov_year_groups))
        return {
            "national_conditional_grants": nat_years_dictionary,
            "provincial_transfers": prov_years_dictionary,
            "snapshot_date": {
                "year": config.GRANTS_LATEST_YEAR,
                "quarter": config.GRANTS_LATEST_QUARTER,
            },
        }

    @classmethod
    def exclude_zeros(cls, values):
        return [d for d in values if d["amount.sum"] != 0]

    @classmethod
    def nat_prov_reducer(cls, accumulator, current_value):
        nat, prov = accumulator
        if PROVINCIAL_CODE.match(current_value["grant.code"]):
            prov.append(current_value)
        else:
            nat.append(current_value)
        return nat, prov

    @classmethod
    def split_nat_prov(cls, values):
        return reduce(cls.nat_prov_reducer, values, ([], []))
