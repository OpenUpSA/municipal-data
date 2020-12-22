
from django.contrib import admin

from .models import Geography


@admin.register(Geography)
class GeographyAdmin(admin.ModelAdmin):
    list_display = ("geo_code", "geo_level", "name",)
