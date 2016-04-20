from wazimap.geo import GeoData as GeoDataBase


class GeoData(GeoDataBase):
    LEVELS = ['municipality', 'district']

    def get_locations(self, search_term, levels=None, year=None):
        # ensure we're limiting levels
        if not levels:
            levels = self.LEVELS
        else:
            levels = set(levels) & set(self.LEVELS)
        levels = ','.join(levels)

        return super(GeoData, self).get_locations(search_term, levels, year)

    def get_locations_from_coords(self, longitude, latitude):
        geos = super(GeoData, self).get_locations_from_coords(longitude, latitude)
        return [g for g in geos if g.level in self.LEVELS]
