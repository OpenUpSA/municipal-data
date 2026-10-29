exports.transformHTML = function(html) {
  let newHtml = "{% load static %}\n" + html;
  newHtml = newHtml.replace(/"(?:\.\.\/)*(js|css|images|fonts)([^"]+)"/g, "\"/static/$1$2\"");
  newHtml = newHtml.replace(/"index.html"/g, '"/"');
  return newHtml;
};

exports.transformDOM = function(window, $) {
  $("title").text("{{ page_title }}");
  $('meta[property="og:title"]').attr("content", "{{ page_title }}");
  $('meta[property="og:image"]').attr("content", '{% static \'webflow/images/municipal-money-opengraph-wide.png\' %}');
  $('meta[property="twitter:title"]').attr("content", "{{ page_title }}");
  $('meta[property="twitter:image"]').attr("content", '{% static \'webflow/images/municipal-money-opengraph-wide.png\' %}');
  $('a[href="contact.html"]').remove();

  [
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>',
    '<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" integrity="sha256-YU3qCpj/P06tdPBJGPax0bm6Q1wltfwjsho5TR4+TYc=" crossorigin=""/>',
    '<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" integrity="sha256-YSWCMtmNZNwqex4CEw1nQhvFub2lmU7vcCKP+XVwwXA=" crossorigin=""/>',
    '<meta name="description" content="{{ page_description }}">',
    '<meta name="twitter:title" content="{{ page_title }}">',
    '<meta name="twitter:description" content="{{ page_description }}">',
    '<meta name="twitter:card" content="page_summary">',
    '<meta name="twitter:site" content="@MunicipalMoney">',
    '<meta property="og:description" content="{{ page_description }}">',
    '{% if NO_INDEX %}<meta name="robots" content="noindex">{% endif %}'
  ].forEach(html => $("head").append(html + "\n"));

  // Body scripts
  addScriptToBody(window, {
    src: "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
    integrity: "sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=",
    crossorigin: "",
  });
  addScriptToBody(window, {
    src: "https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js",
    integrity: "sha256-Hk4dIpcqOSb0hZjgyvFOP+cEmDXUKKNE/tT542ZbNQg=",
    crossorigin: "",
  });

  addScriptToBody(window, {src: "/static/js/utils.js"});
  addScriptToBody(window, {src: "/static/js/mm-webflow.js"});
  addScriptToBody(window, {src: "/static/js/humanize.js"});
  addScriptToBody(window, {src: "{% static 'household/js/plotly.js' %}"});

  addScriptToBody(window, {}, "function amount_convert(value){\
    var total = Humanize.compactInteger(value[0], 1);\
    return 'Spent in '+ value + '<br>' + 'R '+ total;\
  }\
  function extract_quarters(data){\
    return data[1];\
  }\
  function add_rand(value){\
    return 'R ' + Humanize.compactInteger(value, 1);\
  }\
  ");

  addScriptToBody(window, {}, "$(document).ready(function() {\
    var chartColors = [\
      '#4fb2db',\
      '#4ba39c',\
      '#7558a6',\
      '#ff73a0',\
      '#ffac54',\
      '#ff9061',\
      '#826a6c',\
      '#5b74d9',\
      '#98ceb4',\
    ];\
    var pageData = {{page_data_json|safe}};\
    var js = JSON.parse(pageData['data']);\
    mmWebflow(js);\
    var original_data = {{original_data|safe}};\
    var adjusted_data = {{adjusted_data|safe}};\
    var quarter_data = {{quarter_data|safe}};\
    var implementation_year = '{{implementation_year|safe}}';\
    if (quarter_data) {\
      data = [];\
      var original_chart = {\
        x: original_data.labels,\
        y: original_data.data,\
        hoverinfo: 'text',\
        text: original_data.data.map(add_rand),\
        type: 'bar',\
        name: 'Original Budget',\
      };\
      data.push(original_chart);\
      var adjusted_chart = {\
        x: adjusted_data.labels,\
        y: adjusted_data.data,\
        hoverinfo: 'text',\
        text: adjusted_data.data.map(add_rand),\
        type: 'bar',\
        name: 'Adjusted Budget',\
      };\
      data.push(adjusted_chart);\
      for (const quarter in quarter_data) {\
        var total = Humanize.compactInteger(quarter_data[quarter][1], 1);\
        var quarter_name = quarter_data[quarter][0];\
        var quarter_chart = {\
          x: ['Quarterly Expenditure'],\
          y: [quarter_data[quarter][1]],\
          type: 'bar',\
          hoverinfo: 'text',\
          text: 'Spent in ' + quarter_name + '<br>' + 'R ' + total,\
          name: quarter_name + ' Spending',\
        };\
        data.push(quarter_chart);\
      }\
      var layout = {\
        margin: {\
          t: 10\
        },\
        barmode: 'stack',\
        xaxis: {\
          title: 'Financial Year ' + implementation_year\
        },\
        colorway: chartColors,\
      };\
      var config = {\
        displayModeBar: false,\
        responsive: true,\
      };\
      Plotly.newPlot('chart', data, layout, config);\
    }\
  });\
  ");

  addScriptToBody(window, {}, "(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){\
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');\
{% if GOOGLE_ANALYTICS_ID %}\
ga('create', '{{ GOOGLE_ANALYTICS_ID }}', 'auto');\
{% endif %}\
ga('send', 'pageview');\
");
  addScriptToBody(window, {
    src: 'https://www.googletagmanager.com/gtag/js?id={{ GOOGLE_GA4_TAG }}',
  });
  addScriptToBody(window, {}, "window.dataLayer = window.dataLayer || [];\
    function gtag() { dataLayer.push(arguments); }\
    gtag('js', new Date());\
    gtag('config', '{{ GOOGLE_GA4_TAG }}');\
  ");

  $(".section:first .container").prepend("{% for notice in site_notices %}<div>{{ notice.content | safe }}</div>{% endfor %}");

  temporary_webflow_fixes($);
};

function addScriptToBody(window, attrs, text) {
  // Adding a script tag to body via jQuery seems to add it to head as well
  const tag = window.document.createElement("script");
  for (let name in attrs)
    tag.setAttribute(name, attrs[name]);
  if (text)
    tag.appendChild(window.document.createTextNode(text));

  window.document.body.appendChild(tag);
  window.document.body.appendChild(window.document.createTextNode("\n"));
}

function temporary_webflow_fixes($) {
  $(".text_subsection-detail").html("<p class='text_subsection-detail'>This chart shows the expenditure of a capital project over a financial year and not over the projects lifetime. The original and adjusted budgets also cover a financial year.\
  <br><br>\
  The quarterly expenditure line goes up by the amount spend in that quarter, subsequent quarters will show a combination of the total spent so far in the year and what was spent in the quarter as well.\
  </p>\
  ");

  var chartWrapper = "{% if quarter_data %}" + $(".subsection-chart_wrapper").html() + "{% else %}<h3 class='project-detail_heading'>No Data Available</h3>{% endif %}";
  $(".subsection-chart_wrapper").html(chartWrapper);
  $("#project-time-series").html("<div id='chart'></div>");

  $("#project-map").css("height", "155px");
  $("#project-map").css("width", "100%");
  $("#project-map").html("");
}