$(function() {
  $.ajax({
    url: "/api/cubes"
    }).done(function(response) {
      $('#get-cubes').text(JSON.stringify(response, null, 2));
    });
});
