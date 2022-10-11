exports.transformHTML = function(html) {
  let newHtml = "{% load static %}\n{% load staticfiles pipeline json_script_escape %}\n" + html;
  newHtml = newHtml.replace(/"(?:\.\.\/)*(js|css|images|fonts)([^"]+)"/g, "\"{% static 'webflow/$1$2' %}\"");
  newHtml = newHtml.replace(/"index.html"/g, '"/"');
  newHtml = newHtml.replace(/"help.html"/g, '"/help"');
  newHtml = newHtml.replace(/"terms.html"/g, '"/terms"');
  newHtml = newHtml.replace(/"locate.html"/g, '"/locate"');
  return newHtml;
};

exports.transformDOM = function(window, $) {
  $("title").text("{{ page_title }}");
  $('meta[property="og:title"]').attr("content", "{{ page_title }}");
  $('meta[property="og:image"]').attr("content", '{% static \'webflow/images/municipal-money-opengraph-wide.png\' %}');
  $('meta[property="twitter:image"]').attr("content", '{% static \'webflow/images/municipal-money-opengraph-wide.png\' %}');
  $('a[href="contact.html"]').remove();

  [
    '<link rel="stylesheet" href="{% static \'scss/municipal-money.css\' %}">',
    '<meta name="description" content="{{ page_description }}">',
    '<meta name="twitter:title" content="{{ page_title }}">',
    '<meta name="twitter:description" content="{{ page_description }}">',
    '<meta name="twitter:card" content="summary">',
    '<meta name="twitter:site" content="@MunicipalMoney">',
    '<meta property="og:description" content="{{ page_description }}">',
    '{% stylesheet "scorecard" %}',
    '{% if NO_INDEX %}<meta name="robots" content="noindex">{% endif %}'
  ].forEach(html => $("head").append(html + "\n"));

  // Body scripts
  addScriptToBody(window, {
    src: "https://browser.sentry-cdn.com/5.27.6/bundle.tracing.min.js",
    integrity: "sha384-9Z8PxByVWP+gIm/rTMPn9BWwknuJR5oJcLj+Nr9mvzk8nJVkVXgQvlLGZ9SIFEJF",
    crossorigin: "anonymous",
  });
  addScriptToBody(window, {
    src: "https://browser.sentry-cdn.com/5.27.6/captureconsole.min.js",
    integrity: "sha384-F9eVzZTC8N8+p6mvSqBoTIuFHbKq2XFPn6ZtNKPkUBslMACSFOHy3/1XkET00hnC",
    crossorigin: "anonymous",
  });
  addScriptToBody(window, {}, '\
  Sentry.init({\
  dsn: "{{ SENTRY_DSN }}",\
  integrations: [\
    new Sentry.Integrations.CaptureConsole({\
      levels: ["error"]\
    }),\
    new Sentry.Integrations.BrowserTracing(),\
  ],\
  tracesSampleRate: 0.1,\
})');
  addScriptToBody(window, {
    id: "page-data",
    type: "application/json"
  }, "{{ page_data_json|json_script_escape:True }}");
  addScriptToBody(window, {}, "var DATA_PORTAL_URL = '{{ DATA_PORTAL_URL }}'");
  window.document.body.appendChild(
    window.document.createTextNode(
      "{% javascript 'scorecard' %}"
    )
  );

  addScriptToBody(window, {src: "{% static 'household/js/plotly.js' %}"});
  addScriptToBody(window, {src: "{% static 'household/js/household.js' %}"});
  addScriptToBody(window, {src: "{% static 'js/municipal-money.js' %}"});
  addScriptToBody(window, {}, "(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){\
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');\
{% if GOOGLE_ANALYTICS_ID %}\
ga('create', '{{ GOOGLE_ANALYTICS_ID }}', 'auto');\
{% endif %}\
ga('send', 'pageview');\
");

$(".site-notice").html(`{% for notice in site_notices %}
  <div class='container'>
    <div class='site-notice__text'>{{ notice.content | safe }}</div>
  </div>
{% endfor %}`);
$(".site-notice").removeClass("hidden");

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
