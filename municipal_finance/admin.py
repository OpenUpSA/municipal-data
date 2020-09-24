import csv
import urllib
import requests

from contextlib import closing
from django.contrib import admin

from .models import ContactsUpload, MunicipalityStaffContacts


@admin.register(ContactsUpload)
class ContactsUploadAdmin(admin.ModelAdmin):
    list_display = ('datetime',)
    fieldnames = [
        'demarcation_code',
        'role',
        'title',
        'name',
        'office_number',
        'fax_number',
        'email_address',
    ]

    def save_model(self, request, obj, form, change):
        super(ContactsUploadAdmin, self).save_model(request, obj, form, change)
        # Read the file
        with closing(requests.get(obj.file.url, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            reader = csv.DictReader(f, fieldnames=self.fieldnames)
            # TODO: Confirm column names
            # Process all the rows in the file
            updated_count = 0
            created_count = 0
            for row in reader:
                if reader.line_num > 1:
                    print(row['demarcation_code'], row['role'])
                    query = MunicipalityStaffContacts.objects.filter(
                        demarcation_code__exact=row['demarcation_code'],
                        role__exact=row['role'],
                    )
                    record = query.first()
                    if record is None:
                        record = MunicipalityStaffContacts(
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
            print(updated_count, created_count)
