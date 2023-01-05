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
    UIFWExpenseFacts,
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
    years = []

    for table in FACT_TABLES:
        years += get_years(table)

    count_years = len(set(years))

    Summary.objects.update_or_create(
        type="years",
        defaults={
            "content": f'{{"count":{count_years}, "min":{min_year}, "max":{max_year}}}'
        },
    )

    total = Geography.objects.all().count()
    metros = Geography.objects.filter(category="A").count()
    munis = Geography.objects.filter(category="B").count()
    districts = Geography.objects.filter(category="C").count()

    Summary.objects.update_or_create(
        type="municipalities",
        defaults={
            "content": f'{{"total":{total}, "metros":{metros}, "munis":{munis}, "districts":{districts}}}'
        },
    )

    for table in FACT_TABLES:
        count_facts += table.objects.all().count()

    Summary.objects.update_or_create(
        type="facts", defaults={"content": f'{{"count":{count_facts}}}'}
    )


def get_years(model):
    years = model.objects.values_list("financial_year", flat=True).distinct()
    return list(years)
