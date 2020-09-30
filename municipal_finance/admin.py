import csv
import urllib
import requests

from argparse import Namespace
from contextlib import closing
from django.contrib import admin
from django_q.tasks import async_task

from .models import MunicipalityStaffContactsUpload, MunicipalityStaffContacts, MunicipalityProfilesRebuild
from .settings import API_URL


def update_municipal_staff_contacts(fieldnames, obj):
    # Read the file
    updated_count = 0
    created_count = 0
    with closing(requests.get(obj.file.url, stream=True)) as r:
        f = (line.decode('utf-8') for line in r.iter_lines())
        reader = csv.DictReader(f, fieldnames=fieldnames)
        # TODO: Confirm column names
        # Process all the rows in the file
        for row in reader:
            if reader.line_num > 1:
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


@admin.register(MunicipalityProfilesRebuild)
class MunicipalityProfilesRebuildAdmin(admin.ModelAdmin):
    list_display = ('datetime',)
    readonly_fields = ('user',)

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ('user',)
        else:
            return super(MunicipalityProfilesRebuildAdmin, self).get_exclude(request, obj)

    def save_model(self, request, obj, form, change):
        # Set the user to the current user
        obj.user = request.user
        # Process default save behavior
        super(MunicipalityProfilesRebuildAdmin, self).save_model(
            request, obj, form, change)
        # Queue task
        async_task(
            'municipal_finance.materialised_views.generate_profiles',
            Namespace(skip=0), API_URL,
            task_name='Rebuild municipality profiles'
        )


@admin.register(MunicipalityStaffContactsUpload)
class ContactsUploadAdmin(admin.ModelAdmin):
    list_display = ('datetime',)
    readonly_fields = ('user',)
    fieldnames = [
        'demarcation_code',
        'role',
        'title',
        'name',
        'office_number',
        'fax_number',
        'email_address',
    ]

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ('user',)
        else:
            return super(ContactsUploadAdmin, self).get_exclude(request, obj)

    def save_model(self, request, obj, form, change):
        # Set the user to the current user
        obj.user = request.user
        # Process default save behavior
        super(ContactsUploadAdmin, self).save_model(request, obj, form, change)
        # Queue task
        async_task(
            'municipal_finance.admin.update_municipal_staff_contacts',
            self.fieldnames, obj, task_name='Municipal staff contacts upload'
        )
