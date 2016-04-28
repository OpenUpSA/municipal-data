// extend the default Wazimap ProfileMaps object to work for us

var BaseProfileMaps = ProfileMaps;
ProfileMaps = function() {
    var self = this;
    this.mapit_url = GeometryLoader.mapit_url;

    _.extend(this, new BaseProfileMaps());

    this.drawAllFeatures = function() {
        var geo_level = this.geo.this.geo_level;
        var geo_code = this.geo.this.geo_code;

        // draw this geometry
        GeometryLoader.loadGeometryForGeo(geo_level, geo_code, function(feature) {
            self.drawFocusFeature(feature);
        });

        // load surrounding map shapes
        GeometryLoader.loadGeometryForLevel('municipality', function(geojson) {
            // we're only interested in municipalities that aren't this feature (already drawn above)
            geojson.features = _.filter(geojson.features, function(f) {
                return f.properties.codes.MDB != geo_code;
            });

            self.drawFeatures(geojson);
        });
    };
};
