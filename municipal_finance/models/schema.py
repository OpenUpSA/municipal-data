from django.db import models


class ItemCodeSchema(models.Model):
    version = models.CharField(max_length=10)

    class Meta:
        abstract = True
