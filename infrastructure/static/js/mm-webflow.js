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

    function populateSummary(container, searchQuery) {
        var facetUrl = "/api/infrastructure/search/facets/?selected_facets=text:" + searchQuery;
        $.ajax(facetUrl, {
            success: function(data, textStatus, jqXHR) {
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
        function Sorter(dropdown) {
            this.state = null;
            this.dropdown = dropdown; 
            this.sortOptions = [
                "Alphabetical (a-z)",
                "Alphabetical (z-a)",
                "Value (descending)",
                "Value (ascending)",
                "Project Status (descending)",
                "Project Status (ascending)",
                "Completion (descending)",
                "Completion (ascending)",
            ];
        }

        Sorter.prototype = {
            initialize: function() {
                var me = this;
                var options = this.dropdown.find("nav .dropdown-link")
                me.template = $(options[0]).clone();
                options.remove();

                this.sortOptions.forEach(function(el) {
                    var option = me.template.clone();
                    $(".dropdown-label", option).text(el);
                    me.dropdown.find("nav").append(option);
                })
                
            }
        }

        function BarChart() {}

        BarChart.prototype = {
            setupBar: function(el, text, val) {
                this.addTooltip(el, text)
                $(".bar", el).css("height", val + "%")
            },

            addTooltip: function(el, text) {
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
        }

        function ProjectTypeBarChart(el) {
            this.barchart = new BarChart()
            this.el = el;
        }

        ProjectTypeBarChart.prototype = {
            update: function(data) {
                var total_count = data.objects.count;
                var barMap = {
                    "New": 0, "Renewal": 1, "Upgrading": 2, "": 3, 
                }

                for (key in barMap) {
                    var idx = barMap[key];
                    this.barchart.setupBar($(".vertical-bar_wrapper:eq(" + idx + ")", this.el), key, 0);
                }

                var typeFacet = data.fields.project_type;

                for (idx in typeFacet) {
                    var key = typeFacet[idx].text;
                    var barID = barMap[key];
                    var count = typeFacet[idx].count;
                    var val = parseInt(count / total_count * 100);
                    var label = key + " - " + val + "%";

                    this.barchart.setupBar($(".vertical-bar_wrapper:eq(" + barID + ")", this.el), label, val);
                }
            }
        }

        function FunctionBarChart(el) {
            this.barchart = new BarChart()
            this.el = el;
        }

        FunctionBarChart.prototype = {
            
            update: function(data) {
                var functionFacet = data.fields["function"];
                var sortedFunctions = functionFacet.sort(function(a, b) {
                    return b.count - a.count;
                })
                var total_count = data.objects.count;


                for (var i = 0; i < 12; i++) {
                    this.barchart.setupBar($(".vertical-bar_wrapper:eq(" + i + ")", this.el), "", 0); 
                }

                for (idx in sortedFunctions) {
                    f = sortedFunctions[idx]
                    var label = f.text;
                    var count = f.count;
                    var val = parseInt(count / total_count * 100);
                    
                    this.barchart.setupBar($(".vertical-bar_wrapper:eq(" + idx + ")", this.el), label, val); 
                }
            }
        }

        function filterDropdown(el, defaultValue) {
            this.el = el;
            this.listeners = {};
            this.defaultValue = defaultValue;
            this.enabled = true;
    
            this.selectedElement = $(".chart-dropdown_trigger", this.el);
            this.optionContainer = this.el.find("nav.chart-dropdown_list");
            this.dropdownItemTemplate = $(".dropdown-link:first", this.optionContainer).clone();
        }

        filterDropdown.prototype = {
            reset: function() {
                // TODO clear filters
                this.setSelected(this.defaultValue);
            },

            setEnabled: function(val) {
                this.enabled = val;
                if (val) {
                    $("div", this.el).css("background-color", "");
                } else {
                    $("div", this.el).css("background-color", "#f7f7f7");
                }
            },

            clearOptions: function() {
                $(this.el).find(".dropdown-link").remove();
            },

            hideOptions: function() {
                this.optionContainer.removeClass("w--open");
            },

            setSelected: function(label) {
                this.selectedElement.find(".text-block").text(label);
            },

            createOption: function(label, ev) {
                var optionElement = this.dropdownItemTemplate.clone();
                var me = this;

                optionElement.click(function() {
                    me.setSelected(label.text);
                    me.hideOptions();
                    ev(label);
                });

                optionElement.find(".search-dropdown_label").text(label.text);
                optionElement.find(".search-dropdown_value").text("");
                if (label.count) {
                    optionElement.find(".search-dropdown_value").text("(" + label.count + ")");
                }

                me.optionContainer.append(optionElement);
            },

            updateDropdown: function(fields, fieldName, plural) {
                var me = this;

                this.clearOptions();

                this.createOption({text: "All " + plural}, function(payload) {
                    payload.fieldName = fieldName; 
                    me.trigger("removefilters", payload);
                });

                fields[fieldName].forEach(function(option) {
                    option.fieldName = fieldName;
                    me.createOption(option, function(payload) {
                        me.trigger("selectedoption", payload);
                    });
                })
            },

            on: function(e, func) {
                if (this.listeners[e] == undefined)
                    this.listeners[e] = [];

                this.listeners[e].push(func)
            },

            trigger: function(e, payload) {
                for (idx in this.listeners[e]) {
                    this.listeners[e][idx](payload);
                }
            }

        }

        function Search(baseUrl) {
            this.baseUrl = baseUrl
            this.selectedFacets = {};
            this.params = new URLSearchParams();
            this.query = "";
        }

        Search.prototype = {
            addFacet: function(key, value) {
                this.selectedFacets[key] = value;
            },

            clearFacets: function(key) {
                if (key != undefined) {
                    delete this.selectedFacets[key];
                } else {
                    this.selectedFacets = {};
                }
            },

            addSearch: function(q) {
                this.query = q;
            },

            clearAll: function(key) {
                this.query = "";
                this.clearFacets();
            },

            createUrl: function() {
                this.params = new URLSearchParams();
                if (this.q != "")
                    this.params.set("q", this.query);

                for (key in this.selectedFacets) {
                    var paramValue = key + "_exact:" + this.selectedFacets[key];
                    this.params.append("selected_facets", paramValue);
                } 

                return this.baseUrl + "?" + this.params.toString();
            }

        }

        function ListView() {
            var me = this;
            this.search = new Search("/api/infrastructure/search/facets/");
            this.searchState = {
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

            this.sorter = new Sorter($("#sorting-dropdown"));
            this.sorter.initialize();
            this.typeBarChart = new ProjectTypeBarChart($("#project-type-summary-chart"));
            this.functionBarChart = new FunctionBarChart($("#project-function-summary-chart"));

            var removeFilters = function(payload) {
                me.search.clearFacets(payload.fieldName);
                var url = me.search.createUrl()
                triggerSearch(url);
            }

            var addFilter = function(payload) {
                me.search.addFacet(payload.fieldName, payload.text);
                var url = me.search.createUrl()
                triggerSearch(url);
            }

            this.provinceDropDown = new filterDropdown($("#province-dropdown"), "All Provinces");
            this.provinceDropDown.on("removefilters", removeFilters);
            this.provinceDropDown.on("selectedoption", addFilter);

            this.municipalityDropDown = new filterDropdown($("#municipality-dropdown"), "All Municipalities");
            this.municipalityDropDown.on("removefilters", removeFilters);
            this.municipalityDropDown.on("selectedoption", addFilter);

            this.typeDropDown = new filterDropdown($("#type-dropdown"), "All Project Types");
            this.typeDropDown.on("removefilters", removeFilters);
            this.typeDropDown.on("selectedoption", addFilter);

            this.functionDropDown = new filterDropdown($("#functions-dropdown"), "All Functions");
            this.functionDropDown.on("removefilters", removeFilters);
            this.functionDropDown.on("selectedoption", addFilter);

            $(".clear-filter__text").on("click", function() {
                // TODO create widget
                $("#Infrastructure-Search-Input").val("");
                me.provinceDropDown.reset();
                me.municipalityDropDown.reset();
                me.typeDropDown.reset();
                me.functionDropDown.reset();
                me.search.clearAll();

                var url = me.search.createUrl()
                triggerSearch(url);
            });

        } 

        ListView.prototype = {
            initialize: function() {
                this.onPageLoaded();
            },

            clearProjectResults: function() {
                $("#result-list-container .narrow-card_wrapper-2").remove();
            },

            onLoading: function() {
                this.clearProjectResults();
                $(".search-detail-value--placeholder").show()
                $(".search-detail-amount--placeholder").show()
                $(".search-detail-value").hide();
                $(".search-detail-amount").hide();
                $(".search-detail__amount").hide();

                this.provinceDropDown.setEnabled(false);
                this.municipalityDropDown.setEnabled(false);
                this.typeDropDown.setEnabled(false);
                this.functionDropDown.setEnabled(false);
            },

            onPageLoaded: function() {
                var me = this;

                // TODO remove this
                $(".list-sorting_wrapper").hide();
                mmListView.resultRowTemplate = $("#result-list-container .narrow-card_wrapper-2:first").clone();
                mmListView.resultRowTemplate.find(".narrow-card_icon").remove();

                mmListView.dropdownItemTemplate = $("#province-dropdown * .dropdown-link:first");
                mmListView.dropdownItemTemplate.find(".search-status").remove();
                mmListView.dropdownItemTemplate.find(".search-dropdown_label").text("");

                this.onLoading(); 
                $("#clear-filters-button").on("click", function() {
                    me.searchState.selectedFacets = {};
                });

            },

            onDataLoaded: function(response) {
                $("#num-matching-projects-field").text("");
                $("#result-list-container .narrow-card_wrapper").remove()

                this.provinceDropDown.setEnabled(true);
                this.municipalityDropDown.setEnabled(true);
                this.typeDropDown.setEnabled(true);
                this.functionDropDown.setEnabled(true);

                this.searchState.noResultsMessage.hide();

                showResults(response);

                this.typeBarChart.update(response);
                this.functionBarChart.update(response);

                this.provinceDropDown.updateDropdown(response.fields, "province", "Provinces");
                this.municipalityDropDown.updateDropdown(response.fields, "geography_name", "Municipalities");
                this.typeDropDown.updateDropdown(response.fields, "project_type", "Project Types");
                this.functionDropDown.updateDropdown(response.fields, "function", "Government Functions");

                $(".search-detail-value--placeholder").hide()
                $(".search-detail-amount--placeholder").hide()
                $(".search-detail-value").show()
                $(".search-detail-amount").show()
                $(".search-detail__amount").show();
            }
        }

    
        var listView = new ListView();
        listView.initialize();

        createTileLayer().addTo(listView.searchState.map);
        listView.searchState.map.addLayer(listView.searchState.markers);

        function buildProjectUrl(project) {
            return listView.searchState.projectsLocation + project.id;
        }

        function createTileLayer() {
            return L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                maxZoom: 18,
                subdomains: 'abc',
            });
        }


        function updateFreeTextParam() {
            listView.searchState.params.set("q", $("#Infrastructure-Search-Input").val());
        }

        function updateFacetParam() {
            listView.searchState.params.delete("selected_facets");
            for (fieldName in listView.searchState.selectedFacets) {
                var paramValue = fieldName + "_exact:" + listView.searchState.selectedFacets[fieldName];
                listView.searchState.params.append("selected_facets", paramValue);
            }
        }

        function buildPagedSearchURL() {
            updateFreeTextParam();
            updateFacetParam();
            return listView.searchState.facetsLocation + "?" + listView.searchState.params.toString();
        }

        function buildAllCoordinatesSearchURL() {
            var params = new URLSearchParams()
            params.set("q", $("#Infrastructure-Search-Input").val());
            for (fieldName in listView.searchState.selectedFacets) {
                params.set(fieldName, listView.searchState.selectedFacets[fieldName])
            }
            // TODO figure this out
            params.set("fields", "url_path,name,latitude,longitude");
            params.set("limit", "1000");
            return listView.searchState.baseLocation + "?" + params.toString();
        }

        function triggerSearch(url) {
            listView.onLoading();
            url = url || buildPagedSearchURL();
            $.get(url)
                .done(function(response) {
                    listView.searchState.nextUrl = response.objects.next;
                    listView.onDataLoaded(response);
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
            listView.searchState.loadingSpinner.show();
            $.get(url)
                .done(function(response) {
                    addMapPoints(response, resetBounds);
                    if (response.next) {
                        getMapPoints(response.next, DONT_RESET_BOUNDS);
                    } else {
                        listView.searchState.loadingSpinner.hide();
                    }
                })
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong when loading map data. Please try again.");
                    console.error( jqXHR, textStatus, errorThrown );
                });
        }

        function showResults(response) {
            $(".search-detail-value").show();
            $(".search-detail__amount").show();
            $("#num-matching-projects-field").text(formatNumber(response.objects.count));
            //$("#search-total-forecast").textformatNumber(formatNumber(543));
            // TODO fix this
            $("#search-total-forecast").text("-");
            var resultItem = mmListView.resultRowTemplate.clone();

            if (response.objects.results.length) {
                listView.clearProjectResults();
                listView.searchState.noResultsMessage.hide();
                response.objects.results.forEach(function(project) {
                    var resultItem = mmListView.resultRowTemplate.clone();
                    var expenditure = project["expenditure"]
                    resultItem.attr("href", buildProjectUrl(project));
                    resultItem.find(".narrow-card_title-2").html(project.project_description);
                    resultItem.find(".narrow-card_middle-column-2:first div").html(project.function);
                    resultItem.find(".narrow-card_middle-column-2:last").html(project.project_type);
                    var amount = "Not available";
                    if (expenditure.length > 0) {
                        amount = formatCurrency(expenditure[0]["amount"]);
                    }
                    resultItem.find(".narrow-card_last-column-2").html(amount);
                    $("#result-list-container").append(resultItem);
                });
            } else {
                listView.searchState.noResultsMessage.show();
            }
        }

        function resetMapPoints() {
            listView.searchState.markers.clearLayers();
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
                listView.searchState.markers.addLayers(markers);
                listView.searchState.map.fitBounds(listView.searchState.markers.getBounds());
            }
        }

         $("#Infrastructure-Search-Input").keypress(function (e) {
            var key = e.which;
            if (key == 13) {  // the enter key code
                listView.searchState.params.set("q", $("#Infrastructure-Search-Input").val());
                // TODO move this into an object
                var query = $("#Infrastructure-Search-Input").val();
                listView.search.addSearch(query);
                var url = listView.search.createUrl()
                triggerSearch(url);
            }
        });
        $("#Search-Button").on("click", triggerSearch);

        $(".load-more_wrapper a").click(function(e) {
            if (listView.searchState.nextUrl.length > 0) {
                triggerSearch(listView.searchState.nextUrl);
            }
        })

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

