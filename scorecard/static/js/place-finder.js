const geocodingAPI = 'https://maps.googleapis.com/maps/api/geocode/json?address=%QUERY&components=country:ZA&region=ZA';
const geoSelect = $('#municipality-search-2, #Municipality-Search-Hero, #municipality-search');

function resultTemplate(info) {
  return `<p class="result-name"><span class="result-type">${info.geo_level}</span>${info.full_name}</p>`;
}

const textMatchEngine = new Bloodhound({
  datumTokenizer(d) { return Bloodhound.tokenizers.whitespace(d.full_name); },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  limit: 20,
  prefetch: {
    url: `${DATA_PORTAL_URL}/api/cubes/municipalities/facts`,
    cache: false,
    transform(data) {
      return _.map(data.data, (d) => {
        const geo_level = d['municipality.category'] == 'C' ? 'district' : 'municipality';
        return {
          geo_level,
          full_name: d['municipality.long_name'],
          full_geoid: `${geo_level}-${d['municipality.demarcation_code']}`,
        };
      });
    },
  },
});
textMatchEngine.initialize();

const geocodeAddressEngine = new Bloodhound({
  datumTokenizer(d) { return Bloodhound.tokenizers.whitespace(d.full_name); },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  limit: 5,
  remote: {
    url: geocodingAPI,
    wildcard: '%QUERY',
    rateLimitWait: 600,
    filter(response) {
      if (response.status != 'OK') return [];

      // collect coords
      const coords = [];
      for (let i = 0; i < response.results.length; i++) {
        const result = response.results[i];
        coords.push({ lat: result.geometry.location.lat, lng: result.geometry.location.lng });
      }

      return coords;
    },
  },
});
geocodeAddressEngine.initialize();

const geocodeEngine = function (query, sync, cb) {
  // first use google to geocode the address, handling caching,
  // the translate coordinates into places using our api
  function found(datums) {
    // now lookup places for these coords
    if (datums.length > 0) {
      const url = `https://mapit.code4sa.org/point/4326/${datums[0].lng},${datums[0].lat}.json?generation=2`;

      $.getJSON(url, (response) => {
        // munis and districts
        let geos = _.filter(_.values(response), (g) => g.type == 'MN' || g.type == 'DC');
        geos = _.map(geos, (g) => {
          const geo_level = g.type == 'MN' ? 'municipality' : 'district';
          return {
            geo_level,
            full_name: g.name,
            full_geoid: `${geo_level}-${g.codes.MDB}`,
          };
        });

        cb(geos);
      });
    }
  }

  geocodeAddressEngine.search(query, found, found);
};

function makeGeoSelectWidget(element, selected) {
  element.typeahead({
    autoselect: true,
    highlight: false,
    hint: false,
    minLength: 2,
  }, {
    // get textual matches from host
    name: 'textmatch',
    displayKey: 'full_name',
    source: textMatchEngine.ttAdapter(),
    limit: 20,
    templates: {
      suggestion: resultTemplate,
    },
  }, {
    // get geocoded matches
    name: 'geocoded',
    displayKey: 'full_name',
    source: geocodeEngine,
    limit: 20,
    templates: {
      suggestion: resultTemplate,
    },
  });

  element.on('typeahead:selected', selected || ((event, datum) => {
    event.stopPropagation();
    window.location = `/profiles/${datum.full_geoid}/`;
  }));
}

makeGeoSelectWidget(geoSelect);
