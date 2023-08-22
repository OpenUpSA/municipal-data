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
from .budget_actual import (
    IncomeTimeSeries,
    IncomeAdjustments,
    SpendingTimeSeries,
    SpendingAdjustments,
)
from .codes import (
    V1_INCOME_LOCAL_CODES,
    V1_INCOME_TRANSFERS_CODES,
    V2_INCOME_LOCAL_CODES,
    V2_INCOME_TRANSFERS_CODES,
    V2_FUNCTIONAL_BREAKDOWN,
)
from collections import defaultdict


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
        SpendingTimeSeries,
        IncomeAdjustments,
        SpendingAdjustments,
    ]
    if has_comparisons is None:
        return calculators
    else:
        return [calc for calc in calculators if calc.has_comparisons == has_comparisons]


def sort_by_year(data):
    for category in data:
        category["values"].sort(key=lambda x: x["year"])
    return sorted(data, key=lambda x: x['category'])


def make_custom_breakdown(api_data):
    func_breakdown = []

    for item in api_data:
        category = V2_FUNCTIONAL_BREAKDOWN[item["function.label"]]
        temp = {
            "function.category_label": category.strip(),
            "financial_year_end.year": item["financial_year_end.year"],
            "amount.sum": item["amount.sum"],
        }
        func_breakdown.append(temp)

    # aggregate amounts from the same categories
    result = []
    temp = {}

    for item in func_breakdown:
        key = (item["function.category_label"], item["financial_year_end.year"])
        if key not in temp:
            temp[key] = item
            result.append(item)
        else:
            temp[key]["amount.sum"] += item["amount.sum"]
    return result


class RevenueSources(IndicatorCalculator):
    name = "revenue_sources"
    has_comparisons = False

    @classmethod
    def get_muni_specifics(cls, api_data):
        year = api_data.years[0]
        v1_data = group_by(api_data.results["revenue_breakdown_v1"], year_key)
        v2_data = group_by(api_data.results["revenue_breakdown_v2"], year_key)

        items = []
        if year in v2_data:
            local_code_list = V2_INCOME_LOCAL_CODES
            items = v2_data[year]
        elif year in v1_data:
            local_code_list = V1_INCOME_LOCAL_CODES
            items = v1_data[year]

        results = {
            "local": {
                "amount": 0,
            },
            "government": {
                "amount": 0,
            },
            "year": year,
            "ref": api_data.references["lges"],
        }
        total = None
        for item in items:
            amount = item["amount.sum"]
            total = add_none_as_zero(total, amount)
            source = "local" if item["item.code"] in local_code_list else "government"
            results[source]["amount"] += amount
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
        v1_groups = [
            ("Property rates", ["0200", "0300"]),
            ("Service Charges", ["0400"]),
            ("Rental income", ["0700"]),
            ("Interest and investments", ["0800", "1000", "1100"]),
            ("Fines", ["1300"]),
            ("Licenses and Permits", ["1400"]),
            ("Agency services", ["1500"]),
            ("Other", ["1700", "1800"]),
        ]
        v2_groups = [
            ("Property rates", ["0200"]),
            ("Service Charges", ["0300", "0400", "0500", "0600"]),
            ("Rental income", ["0800"]),
            ("Interest and investments", ["0900", "1000", "1100"]),
            ("Fines", ["1200"]),
            ("Licenses and Permits", ["1300"]),
            ("Agency services", ["1400"]),
            ("Other", ["1600", "1700"]),
        ]
        v1_results = defaultdict(lambda: dict())
        v2_results = defaultdict(lambda: dict())
        for item in api_data.results["revenue_breakdown_v1"]:
            v1_results[year_key(item)][item["item.code"]] = item
        for item in api_data.results["revenue_breakdown_v2"]:
            v2_results[year_key(item)][item["item.code"]] = item

        year = api_data.years[0]
        if year in v2_results:
            results = v2_results
            groups = v2_groups
        else:
            results = v1_results
            groups = v1_groups

        values = []
        year_name = "%d" % year
        amount_type = "AUDA"
        for label, codes in groups:
            amount = 0
            has_valid_result = False
            for code in codes:
                try:
                    amount += results[year][code]["amount.sum"]
                    has_valid_result = True
                except KeyError:
                    pass
            if has_valid_result:
                values.append(
                    {
                        "item": label,
                        "amount": amount,
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
        v1_results = group_by(api_data.results["expenditure_breakdown_v1"], year_key)
        v2_results = group_by(api_data.results["expenditure_breakdown_v2"], year_key)

        values = []

        for year in api_data.years:
            try:
                if year in v2_results:
                    results = v2_results[year]
                    contracting_code = "2700"
                else:
                    results = v1_results[year]
                    contracting_code = "4200"

                total = sum(x["amount.sum"] for x in results)
                contracting_items = [
                    x["amount.sum"]
                    for x in results
                    if x["item.code"] == contracting_code
                ]
                contracting = percent(contracting_items[0], total)
                # Prefer KeyError but crash before we use it in case we have more than expectexd
                assert len(contracting_items) <= 1

            except (KeyError, IndexError):
                contracting = None

            values.append(
                {
                    "date": year,
                    "result": contracting,
                    "rating": "",
                }
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
        v1_results = group_by(api_data.results["expenditure_breakdown_v1"], year_key)
        v2_results = group_by(api_data.results["expenditure_breakdown_v2"], year_key)

        values = []

        for year in api_data.years:
            try:
                if year in v2_results:
                    results = v2_results[year]
                    staff_codes = ["2000"]
                else:
                    results = v1_results[year]
                    staff_codes = ["3000", "3100"]

                total = sum(x["amount.sum"] for x in results)
                by_item = group_by(results, lambda x: x["item.code"])
                staff_total = 0
                for code in staff_codes:
                    staff_total += by_item[code][0]["amount.sum"]
                    assert len(by_item[code]) == 1

                staff = percent(staff_total, total)
            except KeyError:
                staff = None

            values.append(
                {
                    "date": year,
                    "result": staff,
                    "rating": "",
                }
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
        # remove overlapping results
        results_v1 = []
        for item in api_data.results["expenditure_functional_breakdown"]:
            if (
                item["financial_year_end.year"] < 2019
                and item["amount_type.code"] == "AUDA"
            ):
                results_v1.append(item)

        results_v2 = []
        for item in api_data.results["expenditure_functional_breakdown_v2"]:
            if item["financial_year_end.year"] >= 2019:
                results_v2.append(item)

        results_v2 = make_custom_breakdown(results_v2)
        results = results_v1 + results_v2

        grouped_results = []
        GAPD_values = defaultdict(int)
        for category, yeargroup in groupby(
            sorted(results, key=lambda x: x["function.category_label"]),
            key=lambda x: x["function.category_label"],
        ):
            yeargroup_list = list(yeargroup)
            if len(yeargroup_list) == 0:
                continue
            tmp_values = []
            for result in yeargroup_list:
                if result["function.category_label"] in GAPD_categories:
                    GAPD_values[result["financial_year_end.year"]] += result["amount.sum"]
                else:
                    tmp_values.append(
                        {
                            "year": result["financial_year_end.year"],
                            "value": result["amount.sum"],
                        }
                    )
            if tmp_values:
                grouped_results.append(
                    {
                        "category": result["function.category_label"],
                        "values": tmp_values,
                    }
                )

        GAPD_result = []
        for k, v in GAPD_values.items():
            tmp_dict = {}
            tmp_dict["year"] = k
            tmp_dict["value"] = v
            GAPD_result.append(tmp_dict)

        grouped_results.append({"category": GAPD_label, "values": GAPD_result})
        return {"values": sort_by_year(grouped_results)}
