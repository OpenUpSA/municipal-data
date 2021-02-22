
from django.db import models


class DemarcationChanges(models.Model):
    TRANSITION_CHOICES = (
        ("disestablished", "Disestablished"),
        ("established", "Established"),
        ("continue", "Continue"),
    )

    date = models.DateField(
        blank=False, null=False,
    )
    old_code = models.TextField(
        blank=False, null=False, db_index=True,
    )
    new_code = models.TextField(
        blank=False, null=False, db_index=True,
    )
    old_code_transition = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        db_index=True,
        choices=TRANSITION_CHOICES,
    )
    new_code_transition = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        db_index=True,
        choices=TRANSITION_CHOICES,
    )

    class Meta:
        verbose_name_plural = "Demarcation Changes"

