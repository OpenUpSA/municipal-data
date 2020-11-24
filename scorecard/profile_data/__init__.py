"""
Municipality Profile data preparation
-------------------------------------
Gather data from the municipal finance API and provide values ready for display
on the page with little further processing.

If the API returns a null value, it can generally be treated as zero. That
happens in this library and nulls that should be zeros should not be
left to the frontend to handle.

The shape of data produced by this library is generally a series of years
or quarters in reverse chronological order with associated values. Only the
years that are to be shown are returned.

If data needed to calculate a value for a given date is missing, an
object is returned for that year with the value being None,
to indicate in the page that it is missing.
"""

from itertools import groupby
import dateutil.parser

from .utils import *
from .year_settings import LAST_AUDIT_QUARTER
from .api_client import ApiClient
from .api_data import ApiData
from .indicator_calculator import IndicatorCalculator
from .current_ratio import CurrentRatio
from .liquidity_ratio import LiquidityRatio
from .current_debtors_collection_rate import CurrentDebtorsCollectionRate


def get_indicator_calculators(has_comparisons=None):
    calculators = [
        CashCoverage,
        OperatingBudgetDifference,
        CapitalBudgetDifference,
        RepairsMaintenance,
        RevenueSources,
        RevenueBreakdown,
        CurrentRatio,
        LiquidityRatio,
        CurrentDebtorsCollectionRate,
        ExpenditureFunctionalBreakdown,
        ExpenditureTrendsContracting,
        ExpenditureTrendsStaff,
        CashAtYearEnd,
        FruitlWastefIrregUnauth,
    ]
    if has_comparisons is None:
        return calculators
    else:
        return [calc for calc in calculators if calc.has_comparisons == has_comparisons]


def get_indicators(api_data):
    indicators = {}
    for indicator_calc in get_indicator_calculators():
        indicators[indicator_calc.indicator_name] = indicator_calc.get_muni_specifics(
            api_data
        )
    return indicators


class CashCoverage(IndicatorCalculator):
    indicator_name = "cash_coverage"
    result_type = "months"
    noun = "coverage"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                cash = api_data.results["cash_flow"]["4200"][year]
                monthly_expenses = api_data.results["op_exp_actual"]["4600"][year] / 12
                result = max(ratio(cash, monthly_expenses, 1), 0)
                if result > 3:
                    rating = "good"
                elif result <= 1:
                    rating = "bad"
                else:
                    rating = "ave"
            except KeyError:
                result = None
                rating = None
            values.append({"date": year, "result": result, "rating": rating})

        return {
            "values": values,
            "ref": api_data.references["solgf"],
            "result_type": cls.result_type,
        }


class OperatingBudgetDifference(IndicatorCalculator):
    indicator_name = "op_budget_diff"
    result_type = "%"
    noun = "underspending or overspending"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                op_ex_budget = api_data.results["op_exp_budget"]["4600"][year]
                op_ex_actual = api_data.results["op_exp_actual"]["4600"][year]
                result = percent(
                    (op_ex_actual - op_ex_budget), op_ex_budget, 1)
                overunder = "under" if result < 0 else "over"
                if abs(result) <= 5:
                    rating = "good"
                elif abs(result) <= 15:
                    rating = "ave"
                elif abs(result) > 15:
                    rating = "bad"
                else:
                    rating = None
            except KeyError:
                result = None
                rating = None
                overunder = None
            values.append(
                {
                    "date": year,
                    "result": result,
                    "overunder": overunder,
                    "rating": rating,
                }
            )

        return {
            "values": values,
            "ref": api_data.references["overunder"],
            "result_type": cls.result_type,
        }


class CapitalBudgetDifference(IndicatorCalculator):
    indicator_name = "cap_budget_diff"
    result_type = "%"
    noun = "underspending or overspending"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                cap_ex_budget = api_data.results["cap_exp_budget"]["4100"][year]
                cap_ex_actual = api_data.results["cap_exp_actual"]["4100"][year]
                result = percent(
                    (cap_ex_actual - cap_ex_budget), cap_ex_budget)
                overunder = "under" if result < 0 else "over"
                if abs(result) <= 5:
                    rating = "good"
                elif abs(result) <= 15:
                    rating = "ave"
                elif abs(result) > 15:
                    rating = "bad"
                else:
                    rating = None
            except KeyError:
                result = None
                rating = None
                overunder = None
            values.append(
                {
                    "date": year,
                    "result": result,
                    "overunder": overunder,
                    "rating": rating,
                }
            )

        return {
            "values": values,
            "ref": api_data.references["overunder"],
            "result_type": cls.result_type,
        }


class RepairsMaintenance(IndicatorCalculator):
    indicator_name = "rep_maint_perc_ppe"
    result_type = "%"
    noun = "spending"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                rep_maint = api_data.results["rep_maint"]["4100"][year]
                ppe = api_data.results["ppe"]["1300"][year]
                invest_prop = api_data.results["invest_prop"]["1401"][year]
                result = percent(rep_maint, (ppe + invest_prop))
                if abs(result) >= 8:
                    rating = "good"
                elif abs(result) < 8:
                    rating = "bad"
                else:
                    rating = None
            except KeyError:
                result = None
                rating = None

            values.append({"date": year, "result": result, "rating": rating})

        return {
            "values": values,
            "ref": api_data.references["circular71"],
            "result_type": cls.result_type,
        }


class RevenueSources(IndicatorCalculator):
    indicator_name = "revenue_sources"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        year = api_data.years[0]
        results = {
            "local": {"amount": 0, "items": [], },
            "government": {"amount": 0, "items": [], },
            "year": year,
            "ref": api_data.references["lges"],
        }
        code_to_source = {
            "0200": "local",
            "0300": "local",
            "0400": "local",
            "0700": "local",
            "0800": "local",
            "1000": "local",
            "1100": "local",
            "1300": "local",
            "1400": "local",
            "1500": "local",
            "1600": "government",
            "1610": "government",
            "1700": "local",
            "1800": "local",
        }
        total = None
        for item in api_data.results["revenue_breakdown"]:
            if item["financial_year_end.year"] != year:
                continue
            if item["amount_type.code"] != "AUDA":
                continue
            if item["item.code"] == "1900":
                total = item["amount.sum"]
                continue
            amount = item["amount.sum"]
            results[code_to_source[item["item.code"]]]["amount"] += amount
            results[code_to_source[item["item.code"]]]["items"].append(item)
        if total is None:
            results["government"]["percent"] = None
            results["government"]["value"] = None
            results["local"]["percent"] = None
            results["local"]["value"] = None
            results["rating"] = "bad"
        else:
            results["government"]["percent"] = percent(
                results["government"]["amount"], total
            )
            local_pct = percent(results["local"]["amount"], total)
            results["local"]["percent"] = local_pct
            if local_pct >= 75:
                results["rating"] = "good"
            elif local_pct >= 50:
                results["rating"] = "ave"
            else:
                results["rating"] = "bad"
        return results


class RevenueBreakdown(IndicatorCalculator):
    indicator_name = "revenue_breakdown"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        groups = [
            ("Property rates", ["0200", "0300"]),
            ("Service Charges", ["0400"]),
            ("Rental income", ["0700"]),
            ("Interest and investments", ["0800", "1000", "1100"]),
            ("Fines", ["1300"]),
            ("Licenses and Permits", ["1400"]),
            ("Agency services", ["1500"]),
            ("Government Transfers for Operating Expenses", ["1600"]),
            ("Government Transfers for Capital Expenses", ["1610"]),
            ("Other", ["1700", "1800"]),
        ]
        results = {}
        # Structure as {'2015': {'1900': {'AUDA': ..., 'ORGB': ...}, '0200': ...}, '2016': ...}
        for item in api_data.results["revenue_breakdown"]:
            if item["financial_year_end.year"] not in results:
                results[item["financial_year_end.year"]] = {}
            if item["item.code"] not in results[item["financial_year_end.year"]]:
                results[item["financial_year_end.year"]
                        ][item["item.code"]] = {}
            results[item["financial_year_end.year"]][item["item.code"]][
                item["amount_type.code"]
            ] = item
        values = []
        for year in api_data.years + [api_data.budget_year]:
            if year == api_data.budget_year:
                year_name = "%s budget" % year
                amount_type = "ORGB"
            else:
                year_name = "%d" % year
                amount_type = "AUDA"
            try:
                total = results[year]["1900"][amount_type]["amount.sum"]
                for (label, codes) in groups:
                    amount = 0
                    for code in codes:
                        amount += results[year][code][amount_type]["amount.sum"]
                    values.append(
                        {
                            "item": label,
                            "amount": amount,
                            "percent": percent(amount, total) if amount else 0,
                            "date": year_name,
                            "amount_type": amount_type,
                        }
                    )
            except KeyError:
                values.append(
                    {
                        "item": None,
                        "amount": None,
                        "percent": None,
                        "date": year_name,
                        "amount_type": amount_type,
                    }
                )

        return {"values": values}


class ExpenditureTrendsContracting(IndicatorCalculator):
    indicator_name = "expenditure_trends_contracting"
    result_type = "%"
    noun = "expenditure"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []

        for year in api_data.years:
            try:
                total = api_data.results["expenditure_breakdown"]["4600"][year]
            except KeyError:
                total = None

            try:
                contracting = percent(
                    api_data.results["expenditure_breakdown"]["4200"][year], total
                )
            except KeyError:
                contracting = None

            values.append(
                {"date": year, "result": contracting, "rating": "", }
            )

        return {
            "values": values,
            "result_type": cls.result_type,
        }


class ExpenditureTrendsStaff(IndicatorCalculator):
    indicator_name = "expenditure_trends_staff"
    result_type = "%"
    noun = "expenditure"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []

        for year in api_data.years:
            try:
                total = api_data.results["expenditure_breakdown"]["4600"][year]
            except KeyError:
                total = None

            try:
                staff = percent(
                    api_data.results["expenditure_breakdown"]["3000"][year]
                    + api_data.results["expenditure_breakdown"]["3100"][year],
                    total,
                )
            except KeyError:
                staff = None

            values.append(
                {"date": year, "result": staff, "rating": "", }
            )

        return {
            "values": values,
            "result_type": cls.result_type,
        }


class ExpenditureFunctionalBreakdown(IndicatorCalculator):
    indicator_name = "expenditure_functional_breakdown"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        GAPD_categories = {
            "Budget & Treasury Office",
            "Executive & Council",
            "Planning and Development",
            "Corporate Services",
        }
        GAPD_label = "Governance, Administration, Planning and Development"

        results = api_data.results["expenditure_functional_breakdown"]
        grouped_results = []

        for year, yeargroup in groupby(results, lambda r: r["financial_year_end.year"]):
            try:
                # Skip an entire year if total is missing, suggesting the year is missing
                total = api_data.results["expenditure_breakdown"]["4600"][year]
                GAPD_total = 0.0
                year_name = (
                    "%d" % year
                    if year != api_data.budget_year
                    else ("%s budget" % year)
                )

                for result in yeargroup:
                    # only do budget for budget year, use AUDA for others
                    if api_data.check_budget_actual(year, result["amount_type.code"]):
                        if result["function.category_label"] in GAPD_categories:
                            GAPD_total += result["amount.sum"]
                        else:
                            grouped_results.append(
                                {
                                    "amount": result["amount.sum"],
                                    "percent": percent(result["amount.sum"], total),
                                    "item": result["function.category_label"],
                                    "date": year_name,
                                }
                            )

                grouped_results.append(
                    {
                        "amount": GAPD_total,
                        "percent": percent(GAPD_total, total),
                        "item": GAPD_label,
                        "date": year_name,
                    }
                )
            except KeyError:
                continue

        grouped_results = sorted(
            grouped_results, key=lambda r: (r["date"], r["item"]))
        return {"values": grouped_results}


class CashAtYearEnd(IndicatorCalculator):
    indicator_name = "cash_at_year_end"
    result_type = "R"
    noun = "cash balance"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        for year in api_data.years:
            try:
                result = api_data.results["cash_flow"]["4200"][year]

                if result > 0:
                    rating = "good"
                elif result <= 0:
                    rating = "bad"
                else:
                    rating = None

                values.append(
                    {"date": year, "result": result, "rating": rating})
            except KeyError:
                values.append({"date": year, "result": None, "rating": "bad"})
        return {
            "values": values,
            "ref": api_data.references["solgf"],
            "result_type": cls.result_type,
        }


class FruitlWastefIrregUnauth(IndicatorCalculator):
    indicator_name = "wasteful_exp"
    result_type = "%"
    noun = "expenditure"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        values = []
        aggregate = {}
        for item, results in api_data.results["wasteful_exp"].items():
            for year, amount in results.items():
                if year in aggregate:
                    aggregate[year] += amount
                else:
                    aggregate[year] = amount

        for year in api_data.uifw_years:
            try:
                op_ex_actual = api_data.results["op_exp_actual"]["4600"][year]
                result = percent(aggregate[year], op_ex_actual)
                rating = None
                if result == 0:
                    rating = "good"
                else:
                    rating = "bad"
            except KeyError:
                result = None
                rating = None

            values.append({"date": year, "result": result, "rating": rating})

        return {
            "values": values,
            "ref": api_data.references["circular71"],
            "result_type": cls.result_type,
        }


class Demarcation(object):
    def __init__(self, api_data):
        self.land_gained = []
        self.land_lost = []
        self.disestablished = False
        self.established_after_last_audit = False
        self.established_within_audit_years = False
        def date_key(x): return x["date.date"]
        # Watch out: groupby's iterator is finicky about seeing things twice.
        # E.g. If you just turn the tuples iterator into a list you only see one
        # item in the group
        for date, group in groupby(api_data.results["disestablished"], date_key):
            if self.disestablished:
                # If this is the second iteration
                raise Exception("Muni disestablished more than once")
            else:
                self.disestablished = True
                self.disestablished_date = date
                self.disestablished_to = [
                    x["new_demarcation.code"] for x in group]
        for date, group in groupby(api_data.results["established"], date_key):
            if self.established_after_last_audit:
                # If this is the second iteration
                raise Exception("Muni established more than once")
            else:
                datetime = dateutil.parser.parse(date)
                year, month = calendar_to_financial(
                    datetime.year, datetime.month)
                quarter = quarter_string(year, month)
                if quarter > LAST_AUDIT_QUARTER:
                    self.established_after_last_audit = True
                if datetime.year in api_data.years:
                    self.established_within_audit_years = True
                self.established_date = date
                self.established_from = [
                    x["old_demarcation.code"] for x in group]
        for date, group in groupby(
            api_data.results["demarcation_involved_new"], date_key
        ):
            self.land_gained.append(
                {
                    "date": date,
                    "changes": [
                        {
                            "change": x["old_code_transition.code"],
                            "demarcation_code": x["old_demarcation.code"],
                        }
                        for x in group
                    ],
                }
            )
        for date, group in groupby(
            api_data.results["demarcation_involved_old"], date_key
        ):
            self.land_lost.append(
                {
                    "date": date,
                    "changes": [
                        {
                            "change": x["new_code_transition.code"],
                            "demarcation_code": x["new_demarcation.code"],
                        }
                        for x in group
                    ],
                }
            )

    def as_dict(self):
        demarcation_dict = {
            "land_gained": self.land_gained,
            "land_lost": self.land_lost,
        }
        if self.disestablished:
            demarcation_dict.update(
                {
                    "disestablished": True,
                    "disestablished_date": self.disestablished_date,
                    "disestablished_to": self.disestablished_to,
                }
            )
        if self.established_after_last_audit or self.established_within_audit_years:
            demarcation_dict.update(
                {
                    "established_after_last_audit": self.established_after_last_audit,
                    "established_within_audit_years": self.established_within_audit_years,
                    "established_date": self.established_date,
                    "established_from": self.established_from,
                }
            )
        return demarcation_dict
