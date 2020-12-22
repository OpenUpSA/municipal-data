
from django.db import models


class UIFWExpenseFacts(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.IntegerField()
    item_code = models.TextField()
    item_label = models.TextField()
    amount = models.BigIntegerField(null=True)

    class Meta:
        db_table = "uifwexp_facts"
        unique_together = (
            (
                "demarcation_code",
                "financial_year",
                "item_code",
            ),
        )
