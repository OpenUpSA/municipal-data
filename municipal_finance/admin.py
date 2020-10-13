from argparse import Namespace
from django.contrib import admin
from django_q.tasks import async_task

from .models import MunicipalityStaffContactsUpload, MunicipalityProfilesRebuild
from .settings import API_URL


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
            'municipal_finance.compile_data.compile_data',
            API_URL,
            task_name='Compile data'
        )


@admin.register(MunicipalityStaffContactsUpload)
class MunicipalityStaffContactsUploadAdmin(admin.ModelAdmin):
    list_display = ('datetime',)
    readonly_fields = ('user',)

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ('user',)
        else:
            return super(MunicipalityStaffContactsUploadAdmin, self).get_exclude(request, obj)

    def save_model(self, request, obj, form, change):
        # Set the user to the current user
        obj.user = request.user
        # Process default save behavior
        super(MunicipalityStaffContactsUploadAdmin,
              self).save_model(request, obj, form, change)
        # Queue task
        async_task(
            'municipal_finance.update.update_municipal_staff_contacts',
            obj,
            task_name='Municipal staff contacts upload',
        )
