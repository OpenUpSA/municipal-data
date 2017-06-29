import logging

from django.db import models
from django.conf import settings
from wazimap.models import GeographyBase
import requests

log = logging.getLogger(__name__)


CATEGORIES = {
    'A': 'metro',
    'B': 'local',
    'C': 'district',
}


class LocationNotFound(Exception):
    pass


class Geography(GeographyBase):
    province_name = models.CharField(max_length=100, null=False)
    province_code = models.CharField(max_length=5, null=False)
    category = models.CharField(max_length=2, null=False)
    miif_category = models.TextField(null=True)

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
            'miif_category': self.miif_category,
            'slug': self.slug,
        })
        return d

    @classmethod
    def find(cls, geo_code, geo_level):
        geo = cls.objects.filter(geo_level=geo_level, geo_code=geo_code).first()
        if not geo:
            raise LocationNotFound("Invalid level, code: %s-%s" % (geo_level, geo_code))
        return geo

    @classmethod
    def get_locations_from_coords(cls, longitude, latitude):
        """
        Returns a list of geographies containing this point.
        """
        url = settings.MAPIT['url'] + '/point/4326/%s,%s?generation=%s' % (longitude, latitude, settings.MAPIT['generation'])
        resp = requests.get(url)
        resp.raise_for_status()

        geos = []
        for feature in resp.json().itervalues():
            try:
                geo = cls.find(feature['codes']['MDB'], feature['type_name'].lower())

                if geo.geo_level not in ['municipality', 'district']:
                    geos.append(geo)
            except LocationNotFound as e:
                log.warn("Couldn't find geo that Mapit gave us: %s" % feature, exc_info=e)

        return geos
