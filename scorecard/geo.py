import logging

from wazimap.geo import GeoData as GeoDataBase, LocationNotFound
from django.conf import settings
import requests

from .models import Geography


class GeoData(GeoDataBase):
    LEVELS = ['municipality', 'district']
    log = logging.getLogger(__name__)

    def __init__(self):
        super(GeoData, self).__init__()
        self.geo_model = Geography
        self.settings = settings.MAPIT

    def _clean_levels(self, levels):
        if not levels:
            return self.LEVELS
        else:
            return list(set(levels) & set(self.LEVELS))

    def get_locations(self, search_term, levels=None, year=None):
        levels = self._clean_levels(levels)
        return super(GeoData, self).get_locations(search_term, levels, year)

    def get_locations_from_coords(self, longitude, latitude, levels=None):
        """
        Returns a list of geographies containing this point.
        """
        levels = self._clean_levels(levels)
        resp = requests.get(self.settings['url'] + '/point/4326/%s,%s?generation=%s' % (longitude, latitude, self.settings['generation']))
        resp.raise_for_status()

        geos = []
        for feature in resp.json().itervalues():
            try:
                geo = self.get_geography(feature['codes']['MDB'],
                                         feature['type_name'].lower())

                if not levels or geo.geo_level in levels:
                    geos.append(geo)
            except LocationNotFound as e:
                self.log.warn("Couldn't find geo that Mapit gave us: %s" % feature, exc_info=e)

        return geos
