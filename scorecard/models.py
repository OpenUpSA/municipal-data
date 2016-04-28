from django.db import models

from wazimap.models import GeographyBase


class Geography(GeographyBase):
    province_name = models.CharField(max_length=100, null=False)
    province_code = models.CharField(max_length=5, null=False)
    category = models.CharField(max_length=2, null=False)

    def as_dict(self):
        d = super(Geography, self).as_dict()
        d.update({
            'province_name': self.province_name,
            'province_code': self.province_code,
            'category': self.category,
        })
        return d
