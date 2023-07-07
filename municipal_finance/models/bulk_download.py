from django.db import models


class BulkDownload(models.Model):
    file_name = models.TextField()

    class Meta:
        db_table = "bulk_doownload"
        verbose_name_plural = "Bulk Downloads"
