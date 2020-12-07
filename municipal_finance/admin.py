from datetime import date
from argparse import Namespace
from django.contrib import admin
from django_q.tasks import async_task
from constance import config

from .models import (
    MunicipalStaffContactsUpdate,
    MunicipalityProfilesCompilation,
    IncomeExpenditureV2Update,
    CashFlowV2Update,
    RepairsMaintenanceV2Update,
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


@admin.register(MunicipalStaffContactsUpdate)
class MunicipalStaffContactsUpdateAdmin(admin.ModelAdmin):
    list_display = ('datetime',)
    readonly_fields = ('user',)

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ('user',)
        else:
            return super(MunicipalStaffContactsUpdateAdmin, self).get_exclude(request, obj)

    def save_model(self, request, obj, form, change):
        # Set the user to the current user
        obj.user = request.user
        # Process default save behavior
        super(MunicipalStaffContactsUpdateAdmin, self).save_model(
            request, obj, form, change
        )
        # Queue task
        if not change:
            async_task(
                'municipal_finance.update.update_municipal_staff_contacts',
                obj,
                task_name='Municipal staff contacts update',
            )


class BaseUpdateAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'deleted', 'inserted',)
    readonly_fields = ('user', 'deleted', 'inserted',)

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ('user',)
        else:
            return super(BaseUpdateAdmin, self).get_exclude(request, obj)


@admin.register(IncomeExpenditureV2Update)
class IncomeExpenditureV2UpdateAdmin(BaseUpdateAdmin):

    def save_model(self, request, obj, form, change):
        # Set the user to the current user
        obj.user = request.user
        # Process default save behavior
        super(IncomeExpenditureV2UpdateAdmin, self).save_model(
            request, obj, form, change
        )
        # Queue task
        if not change:
            async_task(
                'municipal_finance.update.update_income_expenditure_v2',
                obj,
                task_name='Income & Expenditure v2 update',
                batch_size=10000,
            )


@admin.register(CashFlowV2Update)
class CashFlowV2UpdateAdmin(BaseUpdateAdmin):

    def save_model(self, request, obj, form, change):
        # Set the user to the current user
        obj.user = request.user
        # Process default save behavior
        super(CashFlowV2UpdateAdmin, self).save_model(
            request, obj, form, change
        )
        # Queue task
        if not change:
            async_task(
                'municipal_finance.update.update_cash_flow_v2',
                obj,
                task_name='Cash flow v2 update',
                batch_size=10000,
            )


@admin.register(RepairsMaintenanceV2Update)
class RepairsMaintenanceV2UpdateAdmin(BaseUpdateAdmin):

    def save_model(self, request, obj, form, change):
        # Set the user to the current user
        obj.user = request.user
        # Process default save behavior
        super(RepairsMaintenanceV2UpdateAdmin, self).save_model(
            request, obj, form, change
        )
        # Queue task
        if not change:
            async_task(
                'municipal_finance.update.update_repairs_maintenance_v2',
                obj,
                task_name='Repairs & Maintenance v2 update',
                batch_size=10000,
            )
