from .indicator_calculator import IndicatorCalculator
from itertools import groupby
from .utils import year_key, group_by
from constance import config
from functools import reduce
import re
from collections import defaultdict


PROVINCIAL_CODE = re.compile("^00\d\d$")


class Grants(IndicatorCalculator):
    name = "grants"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        values_v1 = cls.exclude_zeros(api_data.results["grants_v1"])
        values_v2 = cls.exclude_zeros(api_data.results["grants_v2"])
        national_grants_v1, provincial_transfers_v1, equitable_share_v1 = cls.split(values_v1)
        national_grants_v2, provincial_transfers_v2, equitable_share_v2 = cls.split(values_v2)

        nat_year_groups = group_by(national_grants_v1, year_key)
        prov_year_groups = group_by(provincial_transfers_v1, year_key)
        esg_year_groups =  group_by(equitable_share_v1, year_key)
        nat_year_groups.update(group_by(national_grants_v2, year_key))
        prov_year_groups.update(group_by(provincial_transfers_v2, year_key))
        esg_year_groups.update(group_by(equitable_share_v2, year_key))

        transfers_data = {
            "national_conditional_grants": nat_year_groups,
            "provincial_transfers": prov_year_groups,
            "equitable_share": esg_year_groups,
        }

        transfers_data["snapshot_date"] = {
            "year": config.GRANTS_LATEST_YEAR,
            "quarter": config.GRANTS_LATEST_QUARTER,
        }

        transfers_data["totals"] = cls.totals(transfers_data)

        return transfers_data

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

    @classmethod
    def totals(cls, transfers_data):
        """dictionary keyed on year, of dictionaries keyed on phase, of dictionaries keyed on type"""

        types = ["national_conditional_grants", "provincial_transfers", "equitable_share"]
        years = defaultdict(lambda: defaultdict(lambda: dict()))
        for type in types:
            for year, yeargroup in transfers_data[type].items():
                if year == transfers_data["snapshot_date"]["year"]:
                    for phase, items in group_by(yeargroup, lambda d: d["amount_type.code"]).items():
                        total = sum([d["amount.sum"] for d in items])
                        years[year][phase][type] = total
        return years
