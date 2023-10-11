
import csv
import requests

from collections import namedtuple
from contextlib import closing

from ..models import (
    MunicipalStaffContacts,
)

from .utils import (
    Updater,
    build_unique_query_params_with_role,
)


MunicipalStaffContactRow = namedtuple(
    "MunicipalStaffContactRow",
    (
        "demarcation_code",
        "role",
        "title",
        "name",
        "office_number",
        "fax_number",
        "email_address",
    )
)


class MunicipalStaffContactsReader(object):

    def __init__(self, data):
        self._reader = csv.reader(data)

    def __iter__(self):
        for row in map(MunicipalStaffContactRow._make, self._reader):
            yield row


class MunicipalStaffContactsUpdater(Updater):
    facts_cls = MunicipalStaffContacts
    reader_cls = MunicipalStaffContactsReader

    def build_unique_query(self, rows):
        return build_unique_query_params_with_role(rows)

    def row_to_obj(self, row: MunicipalStaffContactRow):
        return self.facts_cls(
            demarcation_code=row.demarcation_code,
            role=row.role,
            title=row.title,
            name=row.name,
            office_number=row.office_number,
            fax_number=row.fax_number,
            email_address=row.email_address,
        )


def update_municipal_staff_contacts(update_obj, batch_size, **kwargs):
    updater = MunicipalStaffContactsUpdater(update_obj, batch_size)
    updater.update()
