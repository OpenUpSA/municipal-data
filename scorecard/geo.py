from wazimap_mapit.geo import GeoData as GeoDataBase
from .models import Geography


class GeoData(GeoDataBase):
    LEVELS = ['municipality', 'district']

    def __init__(self):
        super(GeoData, self).__init__()
        self.geo_model = Geography

    def _clean_levels(self, levels):
        if not levels:
            return self.LEVELS
        else:
            return list(set(levels) & set(self.LEVELS))

    def get_locations(self, search_term, levels=None, year=None):
        levels = self._clean_levels(levels)
        return super(GeoData, self).get_locations(search_term, levels, year)

    def get_locations_from_coords(self, longitude, latitude, levels=None):
        levels = self._clean_levels(levels)
        return super(GeoData, self).get_locations_from_coords(longitude, latitude, levels)
