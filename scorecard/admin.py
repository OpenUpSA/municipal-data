
from django.contrib import admin

from .models import Geography


@admin.register(Geography)
class GeographyAdmin(admin.ModelAdmin):
    pass
