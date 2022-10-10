browserWidth = document.documentElement.clientWidth;

/*
 * A class that loads geography boundary information from
 * mapit.code4sa.org.
 */
const MAPIT = {
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
  const self = this;
  self.mapit_url = 'https://mapit.code4sa.org';

  this.decorateFeature = function (feature) {
    feature.properties.level = feature.properties.type_name.toLowerCase();
    feature.properties.code = feature.properties.codes.MDB;
    feature.properties.geoid = `${feature.properties.level}-${feature.properties.code}`;
  };

  this.loadGeometryForLevel = function (level, success) {
    let url = `/areas/${MAPIT.level_codes[level]}.geojson?generation=2`;
    const simplify = MAPIT.level_simplify[MAPIT.level_codes[level]];
    if (simplify) {
      url = `${url}&simplify_tolerance=${simplify}`;
    }

    $.getJSON(this.mapit_url + url, (geojson) => {
      const features = _.values(geojson.features);
      _.each(features, self.decorateFeature);
      success({ features });
    }).fail((error) => console.warn(error));
  };

  this.loadGeometryForGeo = function (geo_level, geo_code, generation, success) {
    const mapit_type = MAPIT.level_codes[geo_level];
    const mapit_simplify = MAPIT.level_simplify[mapit_type];
    const url = `/area/MDB:${geo_code}/feature.geojson?generation=${generation}&simplify_tolerance=${mapit_simplify
    }&type=${mapit_type}`;

    $.getJSON(this.mapit_url + url, (feature) => {
      self.decorateFeature(feature);
      success(feature);
    }).fail((error) => console.warn(error));
  };
}
GeometryLoader = new MapItGeometryLoader();

const Maps = function () {
  const self = this;
  this.mapit_url = GeometryLoader.mapit_url;

  this.featureGeoStyle = {
    fillColor: '#66c2a5',
    color: '#777',
    weight: 2,
    opacity: 0.3,
    fillOpacity: 0.5,
    clickable: false,
  };

  this.layerStyle = {
    clickable: true,
    color: '#00d',
    fillColor: '#ccc',
    weight: 1.0,
    opacity: 0.3,
    fillOpacity: 0.3,
  };

  this.hoverStyle = {
    fillColor: '#66c2a5',
    fillOpacity: 0.7,
  };

  this.drawMapsForProfile = function (container, geo, demarcation) {
    this.geo = geo;
    this.createMap(container);
    this.addImagery();

    // for 2011 munis, we load generation 1 maps, otherwise we load 2016 (generation 2) maps
    let generation = 2;
    if (demarcation.disestablished) {
      generation = 1;
      this.featureGeoStyle.fillColor = '#fdcd58';
      this.featureGeoStyle.fillOpacity = 0.7;
      this.featureGeoStyle.color = '#fdcd58';
      this.featureGeoStyle.opacity = 1.0;
    }

    // draw this geometry
    GeometryLoader.loadGeometryForGeo(this.geo.geo_level, this.geo.geo_code, generation, (feature) => {
      self.drawFocusFeature(feature);
    });

    this.drawMunicipalities();
  };

  this.drawMapForHomepage = function (container, centre, zoom) {
    this.createMap(container);
    this.addImagery();

    if (centre) {
      self.map.setView(centre, zoom);
    }

    this.drawMunicipalities();
  };

  this.createMap = function (container) {
    /* Disable map drag on narrow, probably-touch-screen devices
       so that they can scroll the page when the map is a large
       part of their device screen, and so that tapping on the map
       registers as selecting a feature (visiting a muni) rather
       than as a map scroll attempt */
    const allowMapDrag = (browserWidth > 480);

    this.map = L.map($(container)[0], {
      scrollWheelZoom: false,
      zoomControl: false,
      doubleClickZoom: false,
      boxZoom: false,
      keyboard: false,
      dragging: allowMapDrag,
      touchZoom: allowMapDrag,
    });

    if (allowMapDrag) {
      this.map.addControl(new L.Control.Zoom({
        position: 'topright',
      }));
    }
  };

  this.addImagery = function () {
    // add imagery
    L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
      subdomains: 'abc',
      maxZoom: 17,
    }).addTo(this.map);
  };

  this.drawMunicipalities = function () {
    const geo_code = this.geo ? this.geo.geo_code : null;

    // draw all local munis
    GeometryLoader.loadGeometryForLevel('municipality', (data) => {
      // don't include this smaller geo, we already have a shape for that
      data.features = _.filter(data.features, (f) => f.properties.codes.MDB != geo_code);

      self.drawFeatures(data);
    });
  };

  this.drawFocusFeature = function (feature) {
    const layer = L.geoJson([feature], {
      style: self.featureGeoStyle,
    });
    this.map.addLayer(layer);
    this.map.fitBounds(layer.getBounds());
    if (browserWidth > 768) {
      this.map.panBy([-270, 0], { animate: false });
    }
  };

  this.drawFeatures = function (features) {
    // draw all others
    return L.geoJson(features, {
      style: this.layerStyle,
      onEachFeature(feature, layer) {
        layer.bindLabel(feature.properties.name, { direction: 'auto' });

        layer.on('mouseover', () => {
          layer.setStyle(self.hoverStyle);
        });
        layer.on('mouseout', () => {
          layer.setStyle(self.layerStyle);
        });
        layer.on('click', () => {
          window.location = `/profiles/${feature.properties.level}-${feature.properties.code}/`;
        });
      },
    }).addTo(this.map);
  };
};
