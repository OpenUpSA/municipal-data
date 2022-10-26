from django.db import models

from .small_auto_field import SmallAutoField
from .amount_type import AmountTypeV2


class Summary(models.Model):
    type = models.TextField(unique=True)
    content = models.TextField()

    class Meta:
        db_table = "data_summaries"
        verbose_name_plural = "Data Summaries"
