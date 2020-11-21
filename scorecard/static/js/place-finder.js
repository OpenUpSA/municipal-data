var geocodingAPI = 'https://maps.googleapis.com/maps/api/geocode/json?address=%QUERY&components=country:ZA&region=ZA',
    geoSelect = $('#municipality-search-2, #municipality-search');

function resultTemplate(info) {
    return '<p class="result-name"><span class="result-type">' + info.geo_level + '</span>' + info.full_name + '</p>';
}

var textMatchEngine = new Bloodhound({
    datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.full_name); },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    limit: 20,
    prefetch: {
        url: API_URL + '/cubes/municipalities/facts',
        cache: false,
        transform: function(data) {
            return _.map(data.data, function(d) {
                var geo_level = d['municipality.category'] == 'C' ? 'district' : 'municipality';
                return {
                    geo_level: geo_level,
                    full_name: d['municipality.long_name'],
                    full_geoid: geo_level + '-' + d['municipality.demarcation_code'],
                };
            });
        },
    },
});
textMatchEngine.initialize();

var geocodeAddressEngine = new Bloodhound({
    datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.full_name); },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    limit: 5,
    remote: {
        url: geocodingAPI,
        wildcard: "%QUERY",
        rateLimitWait: 600,
        filter: function(response) {
            if (response.status != 'OK') return [];

            // collect coords
            var coords = [];
            for (var i = 0; i < response.results.length; i++) {
                var result = response.results[i];
                coords.push({'lat': result.geometry.location.lat, 'lng': result.geometry.location.lng});
            }

            return coords;
        }
    },
});
geocodeAddressEngine.initialize();

var geocodeEngine = function(query, sync, cb) {
    // first use google to geocode the address, handling caching,
    // the translate coordinates into places using our api
    function found(datums) {
        // now lookup places for these coords
        if (datums.length > 0) {
            var url = 'https://mapit.code4sa.org/point/4326/' + datums[0].lng + ',' + datums[0].lat + '.json?generation=2';

            $.getJSON(url, function(response) {
                // munis and districts
                var geos = _.filter(_.values(response), function(g) { return g.type == "MN" || g.type == "DC"; });
                geos = _.map(geos, function(g) {
                    var geo_level = g.type == "MN" ? "municipality" : "district";
                    return {
                        geo_level: geo_level,
                        full_name: g.name,
                        full_geoid: geo_level + '-' + g.codes.MDB,
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
        minLength: 2
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

    element.on('typeahead:selected', selected || function(event, datum) {
        event.stopPropagation();
        window.location = '/profiles/' + datum.full_geoid + '/';
    });
}

makeGeoSelectWidget(geoSelect);
