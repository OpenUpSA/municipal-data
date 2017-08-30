/*
 * A class that loads geography boundary information from
 * mapit.code4sa.org.
 */
var MAPIT = {
  level_codes: {
    ward: 'WD',
    municipality: 'MN',
    district: 'DC',
    province: 'PR',
    country: 'CY',
  },
  level_simplify: {
    DC: 0.01,
    PR: 0.005,
    MN: 0.005,
    WD: 0.0001,
  },
};

function MapItGeometryLoader() {
  var self = this;
  self.mapit_url = 'https://mapit.code4sa.org';

  this.decorateFeature = function(feature) {
    feature.properties.level = feature.properties.type_name.toLowerCase();
    feature.properties.code = feature.properties.codes.MDB;
    feature.properties.geoid = feature.properties.level + '-' + feature.properties.code;
  };

  this.loadGeometryForLevel = function(level, success) {
    var url = '/areas/' + MAPIT.level_codes[level] + '.geojson?generation=2';
    var simplify = MAPIT.level_simplify[MAPIT.level_codes[level]];
    if (simplify) {
      url = url + '&simplify_tolerance=' + simplify;
    }

    d3.json(this.mapit_url + url, function(error, geojson) {
      if (error) return console.warn(error);
      var features = _.values(geojson.features);
      _.each(features, self.decorateFeature);
      success({features: features});
    });
  };

  this.loadGeometryForGeo = function(geo_level, geo_code, generation, success) {
    var mapit_type = MAPIT.level_codes[geo_level];
    var mapit_simplify = MAPIT.level_simplify[mapit_type];
    var url = "/area/MDB:" + geo_code + "/feature.geojson?generation=" + generation + "&simplify_tolerance=" + mapit_simplify +
      "&type=" + mapit_type;

    d3.json(this.mapit_url + url, function(error, feature) {
      if (error) return console.warn(error);
      self.decorateFeature(feature);
      success(feature);
    });
  };
}
GeometryLoader = new MapItGeometryLoader();


var Maps = function() {
  var self = this;
  this.mapit_url = GeometryLoader.mapit_url;

  this.featureGeoStyle = {
    "fillColor": "rgb(239,125,0)",
    "color": "#777",
    "weight": 2,
    "opacity": 0.3,
    "fillOpacity": 0.5,
    "clickable": false
  };

  this.layerStyle = {
    "clickable": true,
    "color": "#00d",
    "fillColor": "#ccc",
    "weight": 1.0,
    "opacity": 0.3,
    "fillOpacity": 0.3,
  };

  this.hoverStyle = {
    "fillColor": "rgb(239,125,0)",
    "fillOpacity": 0.7,
  };

  this.drawMapsForProfile = function(geo, demarcation) {
    this.geo = geo;
    this.createMap();
    this.addImagery();

    // for 2011 munis, we load generation 1 maps, otherwise we load 2016 (generation 2) maps
    var generation = 2;
    if (demarcation.disestablished) {
      generation = 1;
      this.featureGeoStyle.fillColor = "#fdcd58";
      this.featureGeoStyle.fillOpacity = 0.7;
      this.featureGeoStyle.color = "#fdcd58";
      this.featureGeoStyle.opacity = 1.0;
    }

    // draw this geometry
    GeometryLoader.loadGeometryForGeo(this.geo.geo_level, this.geo.geo_code, generation, function(feature) {
      self.drawFocusFeature(feature);
    });

    this.drawMunicipalities();
  };

  this.drawMapForHomepage = function(centre, zoom) {
    // draw a homepage map, but only for big displays
    if (browserWidth < 768 || $('#slippy-map').length === 0) return;

    this.createMap();
    this.addImagery();

    if (centre) {
      self.map.setView(centre, zoom);
    }

    this.drawMunicipalities();
  };

  this.createMap = function() {
    var allowMapDrag = (browserWidth > 480) ? true : false;

    this.map = L.map('slippy-map', {
      scrollWheelZoom: false,
      zoomControl: false,
      doubleClickZoom: false,
      boxZoom: false,
      keyboard: false,
      dragging: allowMapDrag,
      touchZoom: allowMapDrag
    });

    if (allowMapDrag) {
      this.map.addControl(new L.Control.Zoom({
        position: 'topright'
      }));
    }
  };

  this.addImagery = function() {
    // add imagery
    L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
      subdomains: 'abc',
      maxZoom: 17
    }).addTo(this.map);
  };

  this.drawMunicipalities = function() {
    var geo_code = this.geo ? this.geo.geo_code : null;

    // draw all local munis
    GeometryLoader.loadGeometryForLevel('municipality', function(data) {
      // don't include this smaller geo, we already have a shape for that
      data.features = _.filter(data.features, function(f) {
        return f.properties.codes.MDB != geo_code;
      });

      self.drawFeatures(data);
    });
  };

  this.drawFocusFeature = function(feature) {
    var layer = L.geoJson([feature], {
      style: self.featureGeoStyle,
    });
    this.map.addLayer(layer);
    this.map.fitBounds(layer.getBounds());
    if (browserWidth > 768) {
      this.map.panBy([-270, 0], {animate: false});
    }
  };

  this.drawFeatures = function(features) {
    // draw all others
    return L.geoJson(features, {
      style: this.layerStyle,
      onEachFeature: function(feature, layer) {
        layer.bindLabel(feature.properties.name, {direction: 'auto'});

        layer.on('mouseover', function() {
          layer.setStyle(self.hoverStyle);
        });
        layer.on('mouseout', function() {
          layer.setStyle(self.layerStyle);
        });
        layer.on('click', function() {
          window.location = '/profiles/' + feature.properties.level + '-' + feature.properties.code + '/';
        });
      },
    }).addTo(this.map);
  };
};
