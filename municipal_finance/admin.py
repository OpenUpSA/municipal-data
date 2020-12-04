from datetime import date
from argparse import Namespace
from django.contrib import admin
from django_q.tasks import async_task
from constance import config

from .models import (
    MunicipalityStaffContactsUpload,
    MunicipalityProfilesCompilation,
)
from .settings import API_URL


@admin.register(MunicipalityProfilesCompilation)
class MunicipalityProfilesCompilationAdmin(admin.ModelAdmin):
    list_display = (
        'datetime',
        'user',
        'last_audit_year',
        'last_opinion_year',
        'last_uifw_year',
        'last_audit_quarter',
    )
    readonly_fields = (
        'user',
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(MunicipalityProfilesCompilationAdmin,
                     self).get_form(request, obj, **kwargs)
        form.base_fields['last_audit_year'].disabled = True
        form.base_fields['last_opinion_year'].disabled = True
        form.base_fields['last_uifw_year'].disabled = True
        form.base_fields['last_audit_quarter'].disabled = True
        form.base_fields['last_audit_year'].initial = config.LAST_AUDIT_YEAR
        form.base_fields['last_opinion_year'].initial = config.LAST_OPINION_YEAR
        form.base_fields['last_uifw_year'].initial = config.LAST_UIFW_YEAR
        form.base_fields['last_audit_quarter'].initial = config.LAST_AUDIT_QUARTER
        return form

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ('user',)
        else:
            return super(MunicipalityProfilesCompilationAdmin, self).get_exclude(request, obj)

    def save_model(self, request, obj, form, change):
        # Set the user to the current user
        obj.user = request.user
        # Process default save behavior
        super(MunicipalityProfilesCompilationAdmin, self).save_model(
            request, obj, form, change)
        # Queue task
        async_task(
            'municipal_finance.compile_data.compile_data',
            API_URL,
            obj.last_audit_year,
            obj.last_opinion_year,
            obj.last_uifw_year,
            obj.last_audit_quarter,
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
