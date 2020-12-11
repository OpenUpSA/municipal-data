from .utils import *
from .indicator_calculator import IndicatorCalculator
from .current_ratio import CurrentRatio
from .liquidity_ratio import LiquidityRatio
from .current_debtors_collection_rate import CurrentDebtorsCollectionRate
from .cash_balance import CashBalance
from .cash_coverage import CashCoverage
from .operating_budget_spending import OperatingBudgetSpending
from .capital_budget_spending import CapitalBudgetSpending
from .repairs_maintenance_spending import RepairsMaintenanceSpending
from .uifw_expenditure import UIFWExpenditure
from .grants import Grants
from .income_budget_actual import IncomeTimeSeries, IncomeAdjustments


def get_indicator_calculators(has_comparisons=None):
    calculators = [
        CashCoverage,
        OperatingBudgetSpending,
        CapitalBudgetSpending,
        RepairsMaintenanceSpending,
        RevenueSources,
        LocalRevenueBreakdown,
        CurrentRatio,
        LiquidityRatio,
        CurrentDebtorsCollectionRate,
        ExpenditureFunctionalBreakdown,
        ExpenditureTrendsContracting,
        ExpenditureTrendsStaff,
        CashBalance,
        UIFWExpenditure,
        Grants,
        IncomeTimeSeries,
        IncomeAdjustments,
    ]
    if has_comparisons is None:
        return calculators
    else:
        return [calc for calc in calculators if calc.has_comparisons == has_comparisons]


class RevenueSources(IndicatorCalculator):
    name = "revenue_sources"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        year = api_data.years[0]
        results = {
            "local": {"amount": 0, },
            "government": {"amount": 0, },
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
        for item in api_data.results["local_revenue_breakdown"]:
            if item["financial_year_end.year"] != year:
                continue
            if item["amount_type.code"] != "AUDA":
                continue
            if item["item.code"] == "1900":
                total = item["amount.sum"]
                continue
            amount = item["amount.sum"]
            results[code_to_source[item["item.code"]]]["amount"] += amount
        results["total"] = total
        if total is None:
            results["government"]["percent"] = None
            results["government"]["amount"] = None
            results["local"]["percent"] = None
            results["local"]["amount"] = None
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


class LocalRevenueBreakdown(IndicatorCalculator):
    name = "local_revenue_breakdown"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        # Excluding transfers so that this only includes locally-generated revenue
        groups = [
            ("Property rates", ["0200", "0300"]),
            ("Service Charges", ["0400"]),
            ("Rental income", ["0700"]),
            ("Interest and investments", ["0800", "1000", "1100"]),
            ("Fines", ["1300"]),
            ("Licenses and Permits", ["1400"]),
            ("Agency services", ["1500"]),
            ("Other", ["1700", "1800"]),
        ]
        results = {}
        # Structure as {'2015': {'1900': {'AUDA': ..., 'ORGB': ...}, '0200': ...}, '2016': ...}
        for item in api_data.results["local_revenue_breakdown"]:
            if item["financial_year_end.year"] not in results:
                results[item["financial_year_end.year"]] = {}
            if item["item.code"] not in results[item["financial_year_end.year"]]:
                results[item["financial_year_end.year"]
                        ][item["item.code"]] = {}
            results[item["financial_year_end.year"]][item["item.code"]][
                item["amount_type.code"]
            ] = item
        values = []
        for year in api_data.years:
            year_name = "%d" % year
            amount_type = "AUDA"
            try:
                for (label, codes) in groups:
                    amount = 0
                    for code in codes:
                        amount += results[year][code][amount_type]["amount.sum"]
                    values.append(
                        {
                            "item": label,
                            "amount": amount,
                            "date": year_name,
                            "amount_type": amount_type,
                        }
                    )
            except KeyError:
                values.append(
                    {
                        "item": None,
                        "amount": None,
                        "date": year_name,
                        "amount_type": amount_type,
                    }
                )

        return {"values": values}


class ExpenditureTrendsContracting(IndicatorCalculator):
    name = "expenditure_trends_contracting"
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
    name = "expenditure_trends_staff"
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
    name = "expenditure_functional_breakdown"
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
