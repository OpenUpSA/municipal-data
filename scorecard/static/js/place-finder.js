var textmatchAPI = '/place-search/json/',
    geocodingAPI = 'https://maps.googleapis.com/maps/api/geocode/json?address=%QUERY&components=country:ZA&region=ZA',
    geoSelect = $('#geography-select, #geography-select-home');

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
                return {
                    geo_level: d['municipality.category'] == 'C' ? 'district' : 'municipality',
                    full_name: d['municipality.long_name'],
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
                if (result.partial_match) continue;

                coords.push({'lat': result.geometry.location.lat, 'lng': result.geometry.location.lng});
            }

            return coords;
        }
    },
});
geocodeAddressEngine.initialize();

var geocodeEngine = function(query, cb) {
    // first use google to geocode the address, handling caching,
    // the translate coordinates into places using our api
    function found(datums) {
        // now lookup places for these coords
        var coords = _.map(datums, function(d) { return d.lat + ',' + d.lng; });
        var url = textmatchAPI + '?coords=' + coords.join('&coords=');
        $.getJSON(url, function(response) {
            cb(response.results);
        });
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
makeGeoSelectWidget($('#compare-place-select'), function(event, datum) {
    var geoId = [profileData.geography.this.geo_level, profileData.geography.this.geo_code].join('-');
    event.stopPropagation();
    window.location = '/compare/' + geoId + '/vs/' + datum.full_geoid + '/';
});
