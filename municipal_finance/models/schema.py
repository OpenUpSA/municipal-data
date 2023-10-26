from django.db import models


class ItemCodeSchema(models.Model):
    version = models.TextField()

    class Meta:
        abstract = True
