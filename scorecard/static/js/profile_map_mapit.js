// extend the default Wazimap ProfileMaps object to work for us
// https://github.com/OpenUpSA/wazimap/blob/master/wazimap/static/js/profile_map.js

const BaseProfileMaps = ProfileMaps;
ProfileMaps = function () {
  const self = this;

  _.extend(this, new BaseProfileMaps());

  this.drawAllFeatures = function () {
    const geo_level = this.geo.this.geo_level;
    const geo_code = this.geo.this.geo_code;

    // draw this geometry
    GeometryLoader.loadGeometryForGeo(geo_level, geo_code, (feature) => {
      self.drawFocusFeature(feature);
    });

    // load surrounding map shapes
    GeometryLoader.loadGeometryForLevel('municipality', (geojson) => {
      // we're only interested in municipalities that aren't this feature (already drawn above)
      geojson.features = _.filter(geojson.features, (f) => f.properties.codes.MDB != geo_code);

      self.drawFeatures(geojson);
    });
  };
};
