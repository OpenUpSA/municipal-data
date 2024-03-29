from django.db import models
import ckeditor.fields as ckeditor_fields
from adminsortable.models import SortableMixin

class SiteNotice(SortableMixin):
    description = models.CharField(max_length=200)
    content = ckeditor_fields.RichTextField()
    notice_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ["notice_order"]

    def __str__(self):
        return self.description
