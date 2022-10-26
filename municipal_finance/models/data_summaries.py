from django.db import models


class Summary(models.Model):
    type = models.TextField(unique=True)
    content = models.TextField()

    class Meta:
        db_table = "data_summaries"
        verbose_name_plural = "Data Summaries"
