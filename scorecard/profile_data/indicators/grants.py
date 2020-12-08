from .indicator_calculator import IndicatorCalculator
from itertools import groupby
from .utils import year_key
from constance import config
from functools import reduce
import re


PROVINCIAL_CODE = re.compile("^00\d\d$")


def group_list_by_year(items):
    """Returns dictionary of lists"""
    grouper = groupby(sorted(items, key=year_key), key=year_key)
    return dict(map(lambda g: (g[0], list(g[1])), grouper))


class Grants(IndicatorCalculator):
    name = "grants"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        values_v1 = cls.exclude_zeros(api_data.results["grants_v1"])
        values_v2 = cls.exclude_zeros(api_data.results["grants_v2"])
        national_grants_v1, provincial_transfers_v1, equitable_share_v1 = cls.split(values_v1)
        national_grants_v2, provincial_transfers_v2, equitable_share_v2 = cls.split(values_v2)

        nat_year_groups = group_list_by_year(national_grants_v1)
        prov_year_groups = group_list_by_year(provincial_transfers_v1)
        esg_year_groups =  group_list_by_year(equitable_share_v1)
        nat_year_groups.update(group_list_by_year(national_grants_v2))
        prov_year_groups.update(group_list_by_year(provincial_transfers_v2))
        esg_year_groups.update(group_list_by_year(equitable_share_v2))

        # Equitable Share should only be one value per year
        for year, items in esg_year_groups.items():
            assert len(list(items)) == 1
        esg_year_groups = {year: items[0] for year, items in esg_year_groups.items()}

        return {
            "national_conditional_grants": nat_year_groups,
            "provincial_transfers": prov_year_groups,
            "equitable_share": esg_year_groups,
            "snapshot_date": {
                "year": config.GRANTS_LATEST_YEAR,
                "quarter": config.GRANTS_LATEST_QUARTER,
            },
        }

    @classmethod
    def exclude_zeros(cls, values):
        return [d for d in values if d["amount.sum"] != 0]

    @classmethod
    def nat_prov_esg_reducer(cls, accumulator, current_value):
        nat, prov, esg = accumulator
        if current_value["grant.code"] == "ESG":
            esg.append(current_value)
        elif PROVINCIAL_CODE.match(current_value["grant.code"]):
            prov.append(current_value)
        else:
            nat.append(current_value)
        return nat, prov, esg

    @classmethod
    def split(cls, values):
        return reduce(cls.nat_prov_esg_reducer, values, ([], [], []))
