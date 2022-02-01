exports.transformHTML = function(html) {
  let newHtml = html;
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
    '<meta name="description" content="{{ page_description }}">',
    '<meta name="twitter:title" content="{{ page_title }}">',
    '<meta name="twitter:description" content="{{ page_description }}">',
    '<meta name="twitter:card" content="page_summary">',
    '<meta name="twitter:site" content="@MunicipalMoney">',
    '<meta property="og:description" content="{{ page_description }}">'
  ].forEach(html => $("head").append(html + "\n"));

  // Body scripts
  addScriptToBody(window, {}, "var pageData = {{ page_data_json|safe }}");
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
