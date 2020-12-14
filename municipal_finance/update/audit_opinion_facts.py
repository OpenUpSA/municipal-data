
import csv

from collections import namedtuple

from ..models import AuditOpinionFacts

from .utils import (
    Updater,
    period_code_details,
    build_unique_query_params_with_year,
)


AuditOpinionFactRow = namedtuple(
    "AuditOpinionFactRow",
    (
        "demarcation_code",
        "financial_year",
        "opinion_code",
        "opinion_label",
    ),
)


class AuditOpinionFactsReader(object):

    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(AuditOpinionFactRow._make, self._reader):
            yield row


class AuditOpinionFactsUpdater(Updater):
    facts_cls = AuditOpinionFacts
    reader_cls = AuditOpinionFactsReader
    references_cls = {}

    def build_unique_query(self, rows):
        return build_unique_query_params_with_year(rows)

    def row_to_obj(self, row):
        return self.facts_cls(
            demarcation_code=row.demarcation_code,
            financial_year=row.financial_year,
            opinion_code=row.opinion_code,
            opinion_label=row.opinion_label,
        )


def update_audit_opinion_facts(update_obj, batch_size):
    updater = AuditOpinionFactsUpdater(update_obj, batch_size)
    updater.update()
