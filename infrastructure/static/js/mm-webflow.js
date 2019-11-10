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

    if (js["view"] == "list")
        mmListView(js)
    else
        alert("could not recognise view")

}

