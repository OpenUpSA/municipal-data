from django.db import models


class BulkDownload(models.Model):
    file = models.FileField(upload_to="bulk_downloads/")

    class Meta:
        db_table = "bulk_doownload"
        verbose_name_plural = "Bulk Downloads"
