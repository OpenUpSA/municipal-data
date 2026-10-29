exports.transformHTML = function(html) {
  let newHtml = "{% load static pipeline %}\n" + html;
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
    '<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">',
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>',
    '<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" integrity="sha256-YU3qCpj/P06tdPBJGPax0bm6Q1wltfwjsho5TR4+TYc=" crossorigin=""/>',
    '<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" integrity="sha256-YSWCMtmNZNwqex4CEw1nQhvFub2lmU7vcCKP+XVwwXA=" crossorigin=""/>',
    '<link rel="stylesheet" href="/static/css/muni-money.webflow.init.css"/>',
    '<meta name="description" content="{{ page_description }}">',
    '<meta name="twitter:title" content="{{ page_title }}">',
    '<meta name="twitter:description" content="{{ page_description }}">',
    '<meta name="twitter:card" content="summary">',
    '<meta name="twitter:site" content="@MunicipalMoney">',
    '<meta property="og:description" content="{{ page_description }}">',
    '{% if NO_INDEX %}<meta name="robots" content="noindex">{% endif %}'
  ].forEach(html => $("head").append(html + "\n"));

  // Body scripts
  addScriptToBody(window, {src: "{% static 'js/humanize.js' %}"});
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

  addContentToBody(window, "{% javascript 'infrastructure' %}");

  addScriptToBody(window, {}, "$(document).ready(function() {\
    var pageData = {{ page_data_json|safe }};\
    var js = JSON.parse(pageData['data']);\
    mmWebflow(js);\
  	})\
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

  $(".cc-last .container").prepend("{% for notice in site_notices %}<div>{{ notice.content | safe }}</div>{% endfor %}");

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

function addContentToBody(window, text) {
  const tag = window.document.createElement("div");
  tag.appendChild(window.document.createTextNode(text));

  window.document.body.appendChild(tag);
  window.document.body.appendChild(window.document.createTextNode("\n"));
}