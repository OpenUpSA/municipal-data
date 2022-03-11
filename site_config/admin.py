from django.contrib import admin
from adminsortable.admin import SortableAdmin
from . import models

admin.site.register(models.SiteNotice, SortableAdmin)