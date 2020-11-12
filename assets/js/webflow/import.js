exports.transformHTML = function(html) {
  let newHtml = "{% load static %}\n{% load json_script_escape %}\n" + html;
  newHtml = newHtml.replace(/"(js|css|images|fonts)\//g, "\"/static/webflow/$1/");
  return newHtml;
};

exports.transformDOM = function(window, $) {
  $("title").text("{{ page_title }}");
  $('meta[property="og:title"]').attr("content", "{{ page_title }}");

  [
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin="">',
    '<link rel="stylesheet" href="{% static \'scss/municipal-money.css\' %}">',
    '<meta name="description" content="{{ page_description }}">',
    '<meta name="twitter:title" content="{{ page_title }}">',
    '<meta name="twitter:description" content="{{ page_description }}">',
    '<meta name="twitter:card" content="summary">',
    '<meta name="twitter:site" content="@MunicipalMoney">',
    '<meta property="og:description" content="{{ page_description }}">',
  ].forEach(html => $("head").append(html + "\n"));

  // Body scripts
  addScriptToBody(window, {
    id: "page-data",
    type: "application/json"
  }, "{{ page_data_json|json_script_escape:True }}");
  addScriptToBody(window, {
    src: "https://unpkg.com/leaflet@1.5.1/dist/leaflet.js",
    integrity: "sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==",
    crossorigin:""
  });
  addScriptToBody(window, {src: "{% static 'js/municipal-money.js' %}"});


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
