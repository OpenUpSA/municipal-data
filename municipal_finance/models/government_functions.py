from django.db import models

from .small_auto_field import SmallAutoField


class GovernmentFunctions(models.Model):
    label = models.TextField()
    category_label = models.TextField()
    subcategory_label = models.TextField()

    class Meta:
        abstract = True


class GovernmentFunctionsV1(GovernmentFunctions):
    code = models.TextField(primary_key=True)

    class Meta:
        db_table = "government_functions"
        verbose_name_plural = "Goverment Functions (v1)"


class GovernmentFunctionsV2(GovernmentFunctions):
    id = SmallAutoField(primary_key=True)
    code = models.TextField(unique=True)

    class Meta:
        db_table = "government_functions_v2"
        verbose_name_plural = "Goverment Functions (v2)"

    def __str__(self):
        return self.code
