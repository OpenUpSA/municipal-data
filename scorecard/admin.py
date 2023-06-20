from django.contrib import admin
from django.conf import settings
from django_q.tasks import async_task
from constance import config
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export.signals import post_import
from import_export.formats import base_formats
from django.dispatch import receiver
from django.core.signals import request_started

from .models import (
    Geography,
    GeographyUpdate,
    MunicipalityProfilesCompilation,
)
from .resources import GeographyResource


@admin.register(Geography)
class GeographyAdmin(ImportExportModelAdmin, ExportMixin):
    resource_class = GeographyResource
    list_display = (
        "geo_code",
        "geo_level",
        "name",
    )

    def get_import_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]


@receiver(post_import, dispatch_uid='post_import')
def post_import(model, **kwargs):
    new_geo = GeographyUpdate()
    new_geo.save()


@admin.register(MunicipalityProfilesCompilation)
class MunicipalityProfilesCompilationAdmin(admin.ModelAdmin):
    list_display = (
        "datetime",
        "user",
        "last_audit_year",
        "last_opinion_year",
        "last_uifw_year",
        "last_audit_quarter",
    )
    readonly_fields = (
        "user",
    )
    change_list_template = 'admin/profile_list_form.html'
    add_form_template = 'admin/profile_add_form.html'

    def get_form(self, request, obj=None, **kwargs):
        form = super(MunicipalityProfilesCompilationAdmin, self).get_form(
            request, obj, **kwargs
        )
        form.base_fields["last_audit_year"].disabled = True
        form.base_fields["last_opinion_year"].disabled = True
        form.base_fields["last_uifw_year"].disabled = True
        form.base_fields["last_audit_quarter"].disabled = True
        form.base_fields["last_audit_year"].initial = config.LAST_AUDIT_YEAR
        form.base_fields["last_opinion_year"].initial = config.LAST_OPINION_YEAR
        form.base_fields["last_uifw_year"].initial = config.LAST_UIFW_YEAR
        form.base_fields["last_audit_quarter"].initial = config.LAST_AUDIT_QUARTER
        return form

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ("user",)
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
            "scorecard.compile_profiles.compile_data",
            settings.API_URL,
            obj.last_audit_year,
            obj.last_opinion_year,
            obj.last_uifw_year,
            obj.last_audit_quarter,
            task_name="Compile municipal profiles"
        )

    @receiver(request_started)
    def admin_opened(sender, **kwargs):
        if config.IS_SCORECARD_COMPILED:
            MunicipalityProfilesCompilation._meta.verbose_name_plural = "Municipality Profile Compilations ✅ Profiles compiled"
        else:
            MunicipalityProfilesCompilation._meta.verbose_name_plural = "Municipality Profile Compilations ❌ Compile required"