function mmWebflow(js) {
    function populateSummary(js, container) {
        var count = parseInt(js["count"]).toLocaleString()
        $(".search-detail-value", container)[0].textContent = count;
    }

    function populateList(container, template, data) {

        var dtProjects = data["results"];
        for (var idx in dtProjects) {

            var dtProject = dtProjects[idx];
            var dtExpenditure = dtProject["expenditure"]

            var newProject = template.cloneNode(true);
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

    function mmListView(js) {
        var nextUrl = js["next"];
        var projects = $(".narrow-card_wrapper");
        var projectContainer = $(".narrow-list_wrapper")
        var projectTemplate = projects[0].cloneNode(true);
        populateSummary(js, $(".filtered-projects-info"))

        projects.remove();

        
        $(".load-more_wrapper a").click(function(e) {
            $.ajax(nextUrl, {
                success: function(data, textStatus, jqXHR) {
                    console.log(data);
                    nextUrl = data["next"];
                    populateList(projectContainer, projectTemplate, data)
                }
            })
        })
        populateList(projectContainer, projectTemplate, js);
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

        coords = [22.735740001000067, -33.77845492599994, 25.178260000000023, -31.688509996999983]


        setFinanceValue($(".finances .outcome"), js["expenditure"], "Audited Outcome");
        setFinanceValue($(".finances .forecast"), js["expenditure"], "Full Year Forecast");

        // TODO take into account the budget year
        setFinanceValue($(".finances .budget1"), js["expenditure"], "Budget Year");
        setFinanceValue($(".finances .budget2"), js["expenditure"], "Budget Year");
        setFinanceValue($(".finances .budget3"), js["expenditure"], "Budget Year");

        setMapCoordinates($(".project-map iframe")[0], coords);

    }

    if (js["view"] == "list")
        mmListView(js)
    else if (js["view"] == "detail")
        mmDetailView(js)
    else
        throw "Could not recognise view - expected list or detail";

}

