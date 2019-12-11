function mmWebflow(js) {
    var deepCopy = true;
    function populateSummary(js, container) {
        var count = parseInt(js["count"]).toLocaleString()
        var count = formatNumber(js["count"])
    }

    function formatUnits(number) {
        if (number >= 10**9) {
            return "bn"
            number = number / 10**9
        } else if (number >= 10**6) {
            return "mil"
        }
        return ""
    }

    function formatHuman(number) {
        if (number >= 10**9) {
            number = number / 10**9
        } else if (number >= 10**6) {
            number = number / 10**6;
        } else {
            return "R" + parseInt(number).toLocaleString();
        }

        return "R" + parseFloat(number).toFixed(1);
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
            this.listeners = {};
            this.state = null;
            this.dropdown = dropdown; 
            this.sortOptions = [
                {label: "Alphabetical (a-z)", value: "project-description"},
                {label: "Alphabetical (z-a)", value: "-project-description"},
                {label: "Value (descending)", value: "-total_forecast_budget"},
                {label: "Value (ascending)", value: "total_forecast_budget"},
                {label: "Project Type (descending)", value: "-project_type"},
                {label: "Project Type (ascending)", value: "project_type"},
                {label: "Function (descending)", value: "-function"},
                {label: "Function (ascending)", value: "function"},
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
                    $(".dropdown-label", option).text(el.label);
                    $(".dropdown-label", option).attr("data-option", el.value);
                    me.dropdown.find("nav").append(option);
                    option.on("click", function(e) {
                        var sortField = $("div", option).data("option")
                        me.trigger("sortchanged", sortField);
                    })
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

        function BarChart() {}

        BarChart.prototype = {
            setupBar: function(el, text, val) {
                this.addTooltip(el, text)
                $(".bar", el).css("height", val + "%")
            },

            addTooltip: function(el, text) {
                $(".chart-tooltip", el).remove();
                var tooltip = $("<div></div>").addClass("chart-tooltip");
                (".bar", el).append(tooltip);
                tooltip.append($("<div></div>").addClass("div-block-16"));
                tooltip.append($("<div></div>").addClass("text-block-5").text(text));
                tooltip.css("display", "none");
                tooltip.css("visibility", "visible");

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
            update: function(response) {
                var total_count = response.count;
                var barMap = {
                    "New": 0, "Renewal": 1, "Upgrading": 2, "": 3, 
                }

                for (key in barMap) {
                    var idx = barMap[key];
                    this.barchart.setupBar($(".vertical-bar_wrapper:eq(" + idx + ")", this.el), key, 0);
                }

                var typeFacet = response.facets.project_types;

                for (idx in typeFacet) {
                    var key = typeFacet[idx].key;
                    var barID = barMap[key];
                    var count = typeFacet[idx].count;
                    var val = parseInt(count / total_count * 100);
                    var label = key + " - " + val + "%";

                    this.barchart.setupBar($(".vertical-bar_wrapper:eq(" + barID + ")", this.el), label, val);
                }
            }
        }

        function FunctionBarChart(el) {
            this.el = el;
            this.addTooltip(el, "");
        }

        FunctionBarChart.prototype = {
            
            update: function(data) {
                var total_count = data.count;
                var functionFacet = data.facets.functions
                var sortedFunctions = functionFacet.sort(function(a, b) {
                    return b.doc_count - a.doc_count;
                })

                for (var idx = 0; idx < 12; idx++) {
                    if (sortedFunctions[idx] != undefined) {
                        f = sortedFunctions[idx]
                        var label = f.key;
                        var count = f.count;
                        var val = parseInt(count / total_count * 100);
                        
                        this.setupBar(idx, label, val); 
                    } else {
                        this.setBarHeight(idx, 0);
                    }
                }
            },

            getBar: function(idx) {
                return $(".vertical-bar_wrapper:eq(" + idx + ")", this.el)
            },

            setBarHeight: function(idx, val) {
                var bar = this.getBar(idx);
                $(".bar", bar).css("height", val + "%")
            },

            setupBar: function(idx, text, val) {
                var self = this;
                var label = text + " - " + val + "%";
                var bar = this.getBar(idx);
                this.setBarHeight(idx, val);
                //$(".bar", bar).css("height", val + "%")

                bar.on("mousemove", function(e) {
                    $(".text-block-5", self.tooltip).text(label);
                    self.tooltip.show();
                    self.tooltip.css("left", (-77 + idx * 30) + "px")
                })
                .on("mouseout", function() {
                    self.tooltip.hide();
                })
            },

            addTooltip: function(el, text) {
                $(".chart-tooltip", el).remove();
                this.tooltip = $("<div></div>").addClass("chart-tooltip");
                $(".progress-chart_wrapper", el).append(this.tooltip);
                this.tooltip.append($("<div></div>").addClass("div-block-16"));
                this.tooltip.append($("<div></div>").addClass("text-block-5").text(text));
                this.tooltip.css("width", "50%");
                this.tooltip.css("bottom", "unset");
                this.tooltip.css("top", "-20px");
                this.tooltip.css("display", "none");
                this.tooltip.css("visibility", "visible");

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

                fields.forEach(function(option) {
                    option.fieldName = fieldName;
                    option.text = option.key;
                    option.count = option.doc_count;
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
            this.order = undefined;
        }

        Search.prototype = {
            addFacet: function(key, value) {
                this.selectedFacets[key] = value;
            },

            addOrder: function(orderField) {
                this.order = orderField;
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
                if (this.query != "" && this.query != undefined)
                    this.params.set("search", this.query);

                for (key in this.selectedFacets) {
                    var paramValue = this.selectedFacets[key];
                    this.params.append(key, paramValue);
                } 

                if (this.order != undefined) {
                    this.params.append("ordering", this.order);
                }

                return this.baseUrl + "?" + this.params.toString();
            }

        }

        function ListView() {
            var me = this;
            this.search = new Search("/search/projects");
            this.searchState = {
                baseLocation: "/search/projects/",
                facetsLocation: "/search/projects/",
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
            this.sorter.on("sortchanged", function(payload) {
                me.search.addOrder(payload);
                triggerSearch();
            });

            this.typeBarChart = new ProjectTypeBarChart($("#project-type-summary-chart"));
            this.functionBarChart = new FunctionBarChart($("#project-function-summary-chart"));

            var removeFilters = function(payload) {
                me.search.clearFacets(payload.fieldName);
                triggerSearch();
            }

            var addFilter = function(payload) {
                me.search.addFacet(payload.fieldName, payload.text);
                triggerSearch();
            }

            this.provinceDropDown = new filterDropdown($("#province-dropdown"), "All Provinces");
            this.municipalityDropDown = new filterDropdown($("#municipality-dropdown"), "All Municipalities");
            this.typeDropDown = new filterDropdown($("#type-dropdown"), "All Project Types");
            this.functionDropDown = new filterDropdown($("#functions-dropdown"), "All Functions");

            [this.provinceDropDown, this.municipalityDropDown, this.typeDropDown, this.functionDropDown].forEach(function(dropdown) {
                dropdown.on("removefilters", removeFilters);
                dropdown.on("selectedoption", addFilter);
            })

            $(".clear-filter__text").on("click", function() {
                $("#Infrastructure-Search-Input").val("");
                me.provinceDropDown.reset();
                me.municipalityDropDown.reset();
                me.typeDropDown.reset();
                me.functionDropDown.reset();
                me.search.clearAll();

                triggerSearch();
            });

        } 

        ListView.prototype = {
            initialize: function() {
                this.onPageLoaded();
            },

            clearProjectResults: function() {
                $("#result-list-container .narrow-card_wrapper-2").remove();
            },

            onLoading: function(clearResults) {
                if (clearResults || clearResults == undefined)
                    this.clearProjectResults();
                $(".search-detail-value--placeholder").show()
                $(".search-detail-amount--placeholder").show()
                $(".search-detail_projects").hide();
                
                this.provinceDropDown.setEnabled(false);
                this.municipalityDropDown.setEnabled(false);
                this.typeDropDown.setEnabled(false);
                this.functionDropDown.setEnabled(false);
            },

            onPageLoaded: function() {
                var me = this;

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

                var facets = response.facets
                this.provinceDropDown.updateDropdown(response.facets.provinces, "province", "Provinces");
                this.municipalityDropDown.updateDropdown(response.facets.municipalities, "municipality", "Municipalities");
                this.typeDropDown.updateDropdown(response.facets.project_types, "project_type", "Project Types");
                this.functionDropDown.updateDropdown(response.facets.functions, "function", "Government Functions");

                // TODO Hack to ensure unit is on the same line as the value
                $(".search-detail__amount").css("display", "flex");
                $(".search-detail-value").css("display", "flex");

                $(".search-detail_projects").show();
                $(".search-detail__amount").show();
                $(".search-detail-value--placeholder").hide()
                $(".search-detail-amount--placeholder").hide()
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
            listView.searchState.params.set("search", $("#Infrastructure-Search-Input").val());
            //listView.searchState.params.set("q", $("#Infrastructure-Search-Input").val());
        }

        function updateFacetParam() {
            listView.searchState.params.delete("selected_facets");
            for (fieldName in listView.searchState.selectedFacets) {
                var paramValue = fieldName + "_exact:" + listView.searchState.selectedFacets[fieldName];
                listView.searchState.params.append("selected_facets", paramValue);
            }
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

        function normaliseResponse(response) {
            response.count = response.facets._filter_province.doc_count;
            var facets = response.facets;

            facets.provinces = response.facets._filter_province.province.buckets;
            facets.municipalities = response.facets._filter_municipality.municipality.buckets;
            facets.project_types = response.facets._filter_project_type.project_type.buckets;
            facets.functions = response.facets._filter_functions.functions.buckets;

            ["provinces", "municipalities", "project_types", "functions"].forEach(function(el) {
                var facet = facets[el];
                facet.forEach(function(el2) {
                    el2.count = el2.doc_count;
                    el2.label = el2.key;
                });
            })

            return response;
        }

        function triggerSearch(url, clearProjects) {
            listView.onLoading(clearProjects);
            var isEvent = (url != undefined && url.type != undefined);
            if (isEvent || url == undefined)
                url = listView.search.createUrl();

            $.get(url)
                .done(function(response) {
                    response = normaliseResponse(response)
                    listView.searchState.nextUrl = response.next;
                    listView.onDataLoaded(response);
                })
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong when searching. Please try again.");
                    console.error( jqXHR, textStatus, errorThrown );
                });
            // TODO re-enable
            //resetMapPoints();
            //getMapPoints(buildAllCoordinatesSearchURL());
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
            $("#num-matching-projects-field").text(formatNumber(response.count));
            $("#search-total-forecast").text(formatHuman(response.facets._filter_total_budget.total_budget.value));
            $(".search-detail__amount .units-label").text(formatUnits(response.facets._filter_total_budget.total_budget.value));
            var resultItem = mmListView.resultRowTemplate.clone();

            if (response.results.length) {
                listView.clearProjectResults();
                listView.searchState.noResultsMessage.hide();
                response.results.forEach(function(project) {
                    var resultItem = mmListView.resultRowTemplate.clone();
                    resultItem.attr("href", buildProjectUrl(project));
                    resultItem.find(".narrow-card_title-2").html(project.project_description);
                    resultItem.find(".narrow-card_middle-column-2:first div").html(project.function);
                    resultItem.find(".narrow-card_middle-column-2:last").html(project.project_type);
                    var amount = "R" + formatNumber(project.total_forecast_budget);
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
                triggerSearch();
            }
        });
        $("#Search-Button").on("click", triggerSearch);

        $(".load-more_wrapper a").click(function(e) {
            if (listView.searchState.nextUrl.length > 0) {
                triggerSearch(listView.searchState.nextUrl, false);
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
        // TODO remove
        $(".breadcrumbs a").attr("href", "/infrastructure/projects");

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

