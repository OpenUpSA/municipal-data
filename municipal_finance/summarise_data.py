from django.db.models import Min, Max
from django_q.tasks import async_task
from django.db import transaction

from municipal_finance.models.data_summaries import Summary

from scorecard.models.geography import Geography
from municipal_finance.models.demarcation_changes import DemarcationChanges
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


def summarise_task(task):
    if task.success:
        async_task(
            "municipal_finance.summarise_data.summarise",
            task_name="Summarise Data",
        )

@transaction.atomic
def summarise():
    min_year = 3000
    max_year = 1000
    count_facts = 0

    for table in FACT_TABLES:
        min_year = get_min(min_year, table)
        max_year = get_max(max_year, table)

    count_years = max_year - min_year + 1
    Summary.objects.update_or_create(
        type='years',
        defaults={
            'content': f'{{"count":{count_years}, "min":{min_year}, "max":{max_year}}}'}
    )

    old_demarcations = DemarcationChanges.objects.values_list(
        "old_code", flat=True
    ).distinct()
    total = (
        Geography.objects.all()
        .exclude(geo_code__in=old_demarcations).count()
    )
    metros = (
        Geography.objects.filter(category="A")
        .exclude(geo_code__in=old_demarcations)
        .count()
    )
    munis = (
        Geography.objects.filter(category="B")
        .exclude(geo_code__in=old_demarcations)
        .count()
    )
    districts = (
        Geography.objects.filter(category="C")
        .exclude(geo_code__in=old_demarcations)
        .count()
    )

    Summary.objects.update_or_create(
        type='municipalities',
        defaults={
            'content': f'{{"total":{total}, "metros":{metros}, "munis":{munis}, "districts":{districts}}}'}
    )

    for table in FACT_TABLES:
        count_facts += table.objects.all().count()

    Summary.objects.update_or_create(
        type='facts',
        defaults={'content': f'{{"count":{count_facts}}}'}
    )


def get_min(current_min, model):
    model_min = model.objects.values('financial_year').aggregate(
        Min('financial_year'))['financial_year__min']
    return min(filter(lambda x: x is not None, [current_min, model_min]))


def get_max(current_max, model):
    model_max = model.objects.values('financial_year').aggregate(
        Max('financial_year'))['financial_year__max']
    return max(filter(lambda x: x is not None, [current_max, model_max]))
