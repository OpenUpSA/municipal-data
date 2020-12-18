
from django.db import models


class MunicipalStaffContacts(models.Model):
    id = models.AutoField(primary_key=True)
    demarcation_code = models.TextField()
    role = models.TextField()
    title = models.TextField(null=True)
    name = models.TextField(null=True)
    office_number = models.TextField(null=True)
    fax_number = models.TextField(null=True)
    email_address = models.TextField(null=True)

    class Meta:
        db_table = "municipal_staff_contacts"
        unique_together = (("demarcation_code", "role"),)
