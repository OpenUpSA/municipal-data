from django.db.models import Min, Max
from django_q.tasks import async_task

from municipal_finance.models.data_summaries import Summary

from scorecard.models.geography import Geography

from municipal_finance.models.cash_flow import (
    CflowFactsV1,
    CflowFactsV2,
)
from municipal_finance.models.income_expenditure import (
    IncexpFactsV1,
    IncexpFactsV2,
)
from municipal_finance.models.financial_position import (
    BsheetFactsV1,
    FinancialPositionFactsV2,
)
from municipal_finance.models.capital import (
    CapitalFactsV1,
    CapitalFactsV2,
)
from municipal_finance.models.grants import (
    ConditionalGrantFactsV1,
    GrantFactsV2,
)
from municipal_finance.models.repairs_maintenance import (
    RepairsMaintenanceFactsV1,
    RepairsMaintenanceFactsV2,
)
from municipal_finance.models.aged_debtor import (
    AgedDebtorFactsV1,
    AgedDebtorFactsV2,
)
from municipal_finance.models.aged_creditor import (
    AgedCreditorFactsV1,
    AgedCreditorFactsV2,
)
from municipal_finance.models.uifw_expense import UIFWExpenseFacts


FACT_TABLES = [
    CflowFactsV1,
    CflowFactsV2,
    IncexpFactsV1,
    IncexpFactsV2,
    BsheetFactsV1,
    FinancialPositionFactsV2,
    CapitalFactsV1,
    CapitalFactsV2,
    ConditionalGrantFactsV1,
    GrantFactsV2,
    RepairsMaintenanceFactsV1,
    RepairsMaintenanceFactsV2,
    AgedDebtorFactsV1,
    AgedDebtorFactsV2,
    AgedCreditorFactsV1,
    AgedCreditorFactsV2,
    UIFWExpenseFacts
]


def compile_complete(task):
    if task.success:
        min_year = 3000
        max_year = 1000
        count_facts = 0

        for table in FACT_TABLES:
            min_year = get_min(min_year, table)
            max_year = get_max(max_year, table)

        count_years = max_year - min_year
        Summary.objects.update_or_create(
            type='years',
            defaults={
                'content': f'{{count:{count_years}, min:{min_year}, max:{max_year}}}'}
        )

        total = Geography.objects.all().count()
        metros = Geography.objects.filter(geo_level='metro').count()
        districts = Geography.objects.filter(geo_level='district').count()
        munis = Geography.objects.filter(geo_level='municipality').count()
        Summary.objects.update_or_create(
            type='municipalities',
            defaults={
                'content': f'{{total:{total}, metros:{metros}, districts:{districts}, munis:{munis}}}'}
        )

        for table in FACT_TABLES:
            count_facts += table.objects.all().count()

        Summary.objects.update_or_create(
            type='facts',
            defaults={'content': f'{{count:{count_facts}}}'}
        )


def get_min(current_min, model):
    model_min = model.objects.values('financial_year').aggregate(
        Min('financial_year'))['financial_year__min']
    return min(filter(lambda x: x is not None, [current_min, model_min]))


def get_max(current_max, model):
    model_max = model.objects.values('financial_year').aggregate(
        Max('financial_year'))['financial_year__max']
    return max(filter(lambda x: x is not None, [current_max, model_max]))
