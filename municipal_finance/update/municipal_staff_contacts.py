
import csv
import requests

from contextlib import closing

from ..models import (
    MunicipalStaffContacts,
)


def update_municipal_staff_contacts(obj):
    # Read the file
    fieldnames = [
        'demarcation_code',
        'role',
        'title',
        'name',
        'office_number',
        'fax_number',
        'email_address',
    ]
    updated_count = 0
    created_count = 0
    with closing(requests.get(obj.file.url, stream=True)) as r:
        f = (line.decode('utf-8') for line in r.iter_lines())
        reader = csv.DictReader(f, fieldnames=fieldnames)
        # TODO: Confirm column names
        # Process all the rows in the file
        for row in reader:
            if reader.line_num > 1:
                query = MunicipalStaffContacts.objects.filter(
                    demarcation_code__exact=row['demarcation_code'],
                    role__exact=row['role'],
                )
                record = query.first()
                if record is None:
                    record = MunicipalStaffContacts(
                        demarcation_code=row['demarcation_code'],
                        role=row['role'],
                        title=row['title'],
                        name=row['name'],
                        office_number=row['office_number'],
                        fax_number=row['fax_number'],
                        email_address=row['email_address'],
                    )
                    record.save(force_insert=True)
                    created_count += 1
                else:
                    # TODO: Determine update extent
                    query.update(
                        title=row['title'],
                        name=row['name'],
                        office_number=row['office_number'],
                        fax_number=row['fax_number'],
                        email_address=row['email_address'],
                    )
                    updated_count += 1
    return {
        "updated": updated_count,
        "created": created_count,
    }
