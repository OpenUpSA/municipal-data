function mmWebflow(js) {
    var deepCopy = true;
    function populateSummary(js, container) {
        var count = parseInt(js["count"]).toLocaleString()
        var count = formatNumber(js["count"])
    }

    function formatNumber(number) {
        return parseInt(number).toLocaleString();
    }

    function formatCurrency(decimalString) {
        if (decimalString == null)
            return "";
        return "R " + Math.round(parseFloat(decimalString)).toLocaleString();
    }

    function populateList(container, template, data) {
        var count = formatNumber(data["count"]);
        $(".search-detail-value").text(count);
        var dtProjects = data["results"];
        for (var idx in dtProjects) {

            var dtProject = dtProjects[idx];
            var dtExpenditure = dtProject["expenditure"]

            var newProject = template.cloneNode(deepCopy);
            // TODO figure out a better way to reverse this url
            newProject.href = "/infrastructure/projects/" + dtProject["id"] + "/";

            $(".narrow-card_title", newProject).text(dtProject["project_description"]);
            var divs = $("div", newProject)

            divs[3].textContent = dtProject["function"]
            divs[4].textContent = dtProject["project_type"]
            if (dtExpenditure.length > 0) {
                divs[6].textContent = dtExpenditure[0]["amount"];
            } else {
                divs[6].textContent = "Not available";
            }

            container.append(newProject);
            
        }
    }

    function updateDropdown(selector, fields, fieldName) {
        var container = $(selector);
        var optionContainer = container.find(".chart-dropdown_list");

        var selectedOption = getSelectedOption(fieldName);
        if (typeof(selectedOption) == "undefined") {
            container.find(".text-block").text("All " + facetPlurals[fieldName]);
        } else {
            container.find(".text-block").text(selectedOption);
            // Add "clear filter" option
            optionElement = dropdownItemTemplate.clone();
            optionElement.find(".search-dropdown_label").text("All " + facetPlurals[fieldName]);
            optionElement.click(function() {
                delete searchState.selectedFacets[fieldName];
                optionContainer.removeClass("w--open");
                triggerSearch();
            });
            optionContainer.append(optionElement);
        }

        var options = fields[fieldName];
        fields[fieldName].forEach(function (option) {
            optionElement = dropdownItemTemplate.clone();
            optionElement.find(".search-dropdown_label").text(option.text);
            if (option.count) {
                optionElement.find(".search-dropdown_value").text("(" + option.count + ")");
            }
            optionElement.click(function() {
                searchState.selectedFacets[fieldName] = option.text;
                optionContainer.removeClass("w--open");
                triggerSearch();
            });
            optionContainer.append(optionElement);
        });
    }

    function populateSummary(container, searchQuery) {
        var facetUrl = "/api/infrastructure/search/facets/?selected_facets=text:" + searchQuery;
        $.ajax(facetUrl, {
            success: function(data, textStatus, jqXHR) {
                console.log(data);
                var provinceDropDown = $("#w-dropdown-toggle-0")
                var itemTemplate = $(".dropdown-link", "#w-dropdown-list-0")[0].cloneNode(deepCopy)
                $(".dropdown-link", "#w-dropdown-list-0").remove();

                for (idx in data["fields"]["province"]) {
                    var el = data["fields"]["province"][idx];
                    var item = itemTemplate.cloneNode(deepCopy);
                    $(".search-dropdown_label", item).text(el["text"]);

                    provinceDropDown.append(item);
                }

            }
        }) 
    }

    function mmListView(js) {
        $(".map__embed-2").hide();
        var resultRowTemplate = $("#result-list-container .narrow-card_wrapper:first").clone();
        resultRowTemplate.find(".narrow-card_icon").remove();

        var dropdownItemTemplate = $("#province-dropdown * .dropdown-link:first");
            dropdownItemTemplate.find(".search-status").remove();
            dropdownItemTemplate.find(".search-dropdown_label").text("");
            dropdownItemTemplate.find(".search-dropdown_value").text("");

        var searchState = {
            baseLocation: "/api/infrastructure/search/",
            facetsLocation: "/api/infrastructure/search/facets/",
            projectsLocation: "/infrastructure/projects/",
            nextUrl: "",
            params: new URLSearchParams(),
            selectedFacets: {},
            map: L.map("map").setView([-30.5595, 22.9375], 4),
            markers: L.markerClusterGroup(),
            noResultsMessage: $("#result-list-container * .w-dyn-empty"), // TODO check this
            loadingSpinner: $(".loading-spinner"), // TODO check this
        };

        var facetPlurals = {
            province: "Provinces",
            geography_name: "Municipalities",
            project_type: "Project Types",
            "function": "Government Functions",
        };


        createTileLayer().addTo(searchState.map);
        searchState.map.addLayer(searchState.markers);

        function buildProjectUrl(project) {
            return searchState.projectsLocation + project.id;
        }

        function createTileLayer() {
            return L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                maxZoom: 18,
                subdomains: 'abc',
            });
        }


        function updateFreeTextParam() {
            searchState.params.set("q", $("#Infrastructure-Search-Input").val());
        }

        function updateFacetParam() {
            searchState.params.delete("selected_facets");
            for (fieldName in searchState.selectedFacets) {
                var paramValue = fieldName + "_exact:" + searchState.selectedFacets[fieldName];
                searchState.params.append("selected_facets", paramValue);
            }
        }

        function buildPagedSearchURL() {
            updateFreeTextParam();
            updateFacetParam();
            return searchState.facetsLocation + "?" + searchState.params.toString();
        }

        function buildAllCoordinatesSearchURL() {
            var params = new URLSearchParams()
            params.set("q", $("#Infrastructure-Search-Input").val());
            for (fieldName in searchState.selectedFacets) {
                params.set(fieldName, searchState.selectedFacets[fieldName])
            }
            // TODO figure this out
            params.set("fields", "url_path,name,latitude,longitude");
            params.set("limit", "1000");
            return searchState.baseLocation + "?" + params.toString();
        }

        function resetResults() {
            $("#num-matching-projects-field").text("");
            $("#result-list-container .narrow-card_wrapper").remove()
            resetDropdown("#province-dropdown");
            resetDropdown("#municipality-dropdown");
            resetDropdown("#type-dropdown");
            resetDropdown("#functions-dropdown");
            searchState.noResultsMessage.hide();
        }

        function triggerSearch(url) {
            url = url || buildPagedSearchURL();
            $.get(url)
                .done(function(response) {
                    searchState.nextUrl = response.objects.next;
                    resetResults();
                    showResults(response);
                })
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong when searching. Please try again.");
                    console.error( jqXHR, textStatus, errorThrown );
                });
            resetMapPoints();
            getMapPoints(buildAllCoordinatesSearchURL());
        }

        function getMapPoints(url, resetBounds) {
            var DONT_RESET_BOUNDS = false
            var RESET_BOUNDS = true
            resetBounds = resetBounds == undefined ? RESET_BOUNDS : resetBounds;
            searchState.loadingSpinner.show();
            $.get(url)
                .done(function(response) {
                    addMapPoints(response, resetBounds);
                    if (response.next) {
                        getMapPoints(response.next, DONT_RESET_BOUNDS);
                    } else {
                        searchState.loadingSpinner.hide();
                    }
                })
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong when loading map data. Please try again.");
                    console.error( jqXHR, textStatus, errorThrown );
                });
        }

        function addTooltip(el, text) {
            $(".chart-tooltip", el).remove();
            var tooltip = $("<div></div>").addClass("chart-tooltip");
            $(".bar", el).append(tooltip);
            tooltip.append($("<div></div>").addClass("div-block-16"));
            tooltip.append($("<div></div>").addClass("text-block-5").text(text));
            tooltip.css("display", "none");

            el.on("mouseover", function(e) {
                tooltip.show();
            })
            .on("mouseout", function() {
                tooltip.hide();
            })
        }

        function setupBar(el, text, val) {
            addTooltip(el, text)
            $(".bar", el).css("height", val + "%")
        }
        function updateCharts() {
            setupBar($(".project-status-overview:eq(0) .vertical-bar_wrapper:eq(0)"), "New - 50%", 50);
            setupBar($(".project-status-overview:eq(0) .vertical-bar_wrapper:eq(1)"), "Upgrading - 20%", 20);
            setupBar($(".project-status-overview:eq(0) .vertical-bar_wrapper:eq(2)"), "Renewal - 30%", 30);
            setupBar($(".project-status-overview:eq(0) .vertical-bar_wrapper:eq(3)"), "60%", 60);
        }

        function showResults(response) {
            $("#num-matching-projects-field").text(formatNumber(response.objects.count));
            $("#search-total-forecast").text(formatNumber(543));
            updateDropdown("#province-dropdown", response.fields, "province");
            updateDropdown("#municipality-dropdown", response.fields, "geography_name");
            updateDropdown("#type-dropdown", response.fields, "project_type");
            updateDropdown("#functions-dropdown", response.fields, "function");
            updateCharts();

            if (response.objects.results.length) {
                searchState.noResultsMessage.hide();
                response.objects.results.forEach(function(project) {
                    var resultItem = resultRowTemplate.clone();
                    var expenditure = project["expenditure"]
                    resultItem.attr("href", buildProjectUrl(project));
                    resultItem.find(".narrow-card_title").html(project.project_description);
                    resultItem.find(".narrow-card_middle-column:first").html(project.function);
                    resultItem.find(".narrow-card_middle-column:last").html(project.project_type);
                    var amount = "Not available";
                    if (expenditure.length > 0) {
                        amount = formatCurrency(expenditure[0]["amount"]);
                    }
                    resultItem.find(".narrow-card_last-column").html(amount);
                    $("#result-list-container").append(resultItem);
                });
            } else {
                searchState.noResultsMessage.show();
            }
        }

        function resetMapPoints() {
            searchState.markers.clearLayers();
        }

        function addMapPoints(response, resetBounds) {
            var markers = [];
            response.results.forEach(function(project) {
                if (! project.latitude || ! project.longitude)
                    return;

                var latitude = parseFloat(project.latitude);
                if (latitude < -34.5916 || latitude > -21.783733) {
                    console.log("Ignoring latitude " + latitude);
                    return;
                }

                var longitude = parseFloat(project.longitude);
                if (longitude < 14.206737 || longitude > 33.074960) {
                    console.log("Ignoring longitude " + longitude);
                    return;
                }

                var marker = L.marker([latitude, longitude])
                    .bindPopup(project.project_description + '<br><a target="_blank" href="' +
                               buildProjectUrl(project) + '">Jump to project</a>');
                markers.push(marker);
            });
            if (markers.length && resetBounds) {
                searchState.markers.addLayers(markers);
                searchState.map.fitBounds(searchState.markers.getBounds());
            }
        }

        function resetDropdown(selector) {
            $(selector).find(".text-block").text("");
            $(selector).find(".dropdown-link").remove();
        }

        function getSelectedOption(fieldName) {
            return searchState.selectedFacets[fieldName];
        }

        function updateDropdown(selector, fields, fieldName) {
            var container = $(selector);
            var optionContainer = container.find(".chart-dropdown_list");

            var selectedOption = getSelectedOption(fieldName);
            if (typeof(selectedOption) == "undefined") {
                container.find(".text-block").text("All " + facetPlurals[fieldName]);
            } else {
                container.find(".text-block").text(selectedOption);
                // Add "clear filter" option
                optionElement = dropdownItemTemplate.clone();
                optionElement.find(".search-dropdown_label").text("All " + facetPlurals[fieldName]);
                optionElement.click(function() {
                    delete searchState.selectedFacets[fieldName];
                    optionContainer.removeClass("w--open");
                    triggerSearch();
                });
                optionContainer.append(optionElement);
            }

            var options = fields[fieldName];
            fields[fieldName].forEach(function (option) {
                optionElement = dropdownItemTemplate.clone();
                optionElement.find(".search-dropdown_label").text(option.text);
                if (option.count) {
                    optionElement.find(".search-dropdown_value").text("(" + option.count + ")");
                }
                optionElement.click(function() {
                    searchState.selectedFacets[fieldName] = option.text;
                    optionContainer.removeClass("w--open");
                    triggerSearch();
                });
                optionContainer.append(optionElement);
            });
        }

         $("#Infrastructure-Search-Input").keypress(function (e) {
            var key = e.which;
            if (key == 13) {  // the enter key code
                triggerSearch();
            }
        });
        $("#Search-Button").on("click", triggerSearch);

        $(".load-more_wrapper a").click(function(e) {
            if (searchState.nextUrl.length > 0) {
                triggerSearch(searchState.nextUrl);
            }
        })


        resetResults();
        triggerSearch()
    }

    function mmDetailView(js) {

        function setValue(selector, val) {
            if (val == "" || val == undefined)
                return selector
                    .text("Not available")
                    .addClass("not-available")
            else
                return selector
                    .text(val)
                    .removeClass("not-available")
        }

        function formatCoordinates(latitude, longitude) {
            if (
                latitude != undefined && latitude != 0
                && longitude != undefined && longitude != 0
            )
                return coordinates = latitude + ", " + longitude
            return ""
        }

        function formatAssetClass(assetClass, assetSubClass) {
            var asset = "";

            if (assetClass != "" && assetClass != undefined)
                asset = assetClass;
            
            if (assetSubClass != "" && assetSubClass != undefined)
                asset += " (" + assetSubClass + ")" ;

            return asset;
        }

        function setMapCoordinates(selector, coords) {
            var url = "https://www.openstreetmap.org/export/embed.html?"
            var params = {
                bbox: coords.join(","),
                layer: "mapnik"
            }
            selector.src = url + $.param(params);
        }

        function createMap(selector, bbox, markers) {
            var map = L.map(selector);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(map);

            map.fitBounds([
              [bbox[3], bbox[2]],
              [bbox[1], bbox[0]],
            ])

            return map;
        }

        function addMarker(map, coords, message) {
            if (coords[0] != undefined && coords[1] != undefined && coords[0] != 0 && coords[1] != 0) {
                marker = L.marker(coords).addTo(map)

                if (message != undefined) {
                    marker
                        .bindPopup(message)
                        .openPopup();
                }
            }
        }

        function formatCurrency(amount) {
            return "R" + parseInt(amount).toLocaleString();
        }

        // TODO change the budget year label currently hardcoded to specific years in the template
        function setFinanceValue(selector, expenses, phase) {
            if (expenses.length == 0)
                return setValue(selector, "")
            else {
                for (var idx in expenses) {
                    var e = expenses[idx];    
                    if (e["budget_phase"] != undefined)
                        if (e["budget_phase"]["name"] == phase)
                            return setValue(selector, formatCurrency(e["amount"]))
                }
                return setValue(selector, "");
            }
        }

        setValue($(".project-description"), js["project_description"]);
        setValue($(".project-number__value"), js["project_number"]);
        
        var classSubclass = formatAssetClass(js["asset_class"], js["asset_subclass"])
        setValue($(".project-details .asset-class"), classSubclass);

        setValue($(".project-details .function"), js["function"]);
        setValue($(".project-details .mtsf-outcome"), js["mtsf_service_outcome"]);
        setValue($(".project-details .iudf"), js["iudf"]);
        setValue($(".project-details .project-type"), js["project_type"]);

        setValue($(".geography .province, .breadcrumbs .province"), js["geography"]["province_name"]);
        setValue($(".geography .municipality, .breadcrumbs .municipality"), js["geography"]["name"]);
        setValue($(".geography .ward"), js["ward_location"]);

        var coordinates = formatCoordinates(js["latitude"], js["longitude"])
        setValue($(".geography .coordinates"), coordinates)

        setFinanceValue($(".finances .outcome"), js["expenditure"], "Audited Outcome");
        setFinanceValue($(".finances .forecast"), js["expenditure"], "Full Year Forecast");

        // TODO take into account the budget year
        setFinanceValue($(".finances .budget1"), js["expenditure"], "Budget Year");
        setFinanceValue($(".finances .budget2"), js["expenditure"], "Budget Year");
        setFinanceValue($(".finances .budget3"), js["expenditure"], "Budget Year");

        $(".project-map iframe").remove()
        map = createMap("project-map", js["geography"]["bbox"], [[js["latitude"], js["longitude"]]])
        addMarker(map, [js["latitude"], js["longitude"]], js["project_description"])

    }

    if (js["view"] == "list")
        mmListView(js)
    else if (js["view"] == "detail")
        mmDetailView(js)
    else
        throw "Could not recognise view - expected list or detail";

}

