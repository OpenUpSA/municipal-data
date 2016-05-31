$(function() {
  var updateDocLinkUrl = function(check) {
    $('a.read-the-docs').each(function(index, el) {
      var href = '#accept-tou';
      if (check.checked) {
        href = '/docs';
      }
      el.setAttribute('href', href);
    });
  };
  var check = $('input[name="accept-tou"]');
  check.on('change', function(e) { updateDocLinkUrl(e.target) });
  // In case JS is late and the user's already clicked
  updateDocLinkUrl(check[0]);
});
