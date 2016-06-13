from django.db import models

from wazimap.models import GeographyBase


CATEGORIES = {
    'A': 'metro',
    'B': 'local',
    'C': 'district',
}


class Geography(GeographyBase):
    province_name = models.CharField(max_length=100, null=False)
    province_code = models.CharField(max_length=5, null=False)
    category = models.CharField(max_length=2, null=False)

    @property
    def category_name(self):
        return CATEGORIES[self.category] + ' municipality'

    def as_dict(self):
        d = super(Geography, self).as_dict()
        d.update({
            'province_name': self.province_name,
            'province_code': self.province_code,
            'category': self.category,
            'category_name': self.category_name,
            'slug': self.slug,
        })
        return d
