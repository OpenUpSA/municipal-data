from django.db import models
from django.core import exceptions
from django.utils.translation import gettext as _


class SmallAutoField(models.AutoField):

    def db_type(self, connection):
        return "smallserial"

    def get_internal_type(self):
        return "PositiveSmallIntegerField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be a short integer."))
