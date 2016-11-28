$(function() {
  $.ajax({
    url: "/api/cubes"
    }).done(function(response) {
      $('#get-cubes').text(JSON.stringify(response, null, 2));
    });
});

(function(exports) {
  "use strict";
  var MainView = Backbone.View.extend({
    el: document,

    events: {
      'click button.accept': 'acceptTOU',
      'click button.decline': 'declineTOU',
    },

    initialize: function() {
      // show terms of use dialog?
      if (!Cookies.get('tou-ok')) {
        $('#terms-modal').modal();
      } else {
        this.acceptTOU();
      }
    },

    showTOU: function() {
      $('#terms-modal').modal();
    },

    acceptTOU: function() {
      Cookies.set('tou-ok', true);
      $('#terms-modal').modal('hide');
      $('#terms-ok').removeClass('hidden');
    },

    declineTOU: function() {
      Cookies.remove('tou-ok');
      window.location = "/";
    }
  });

  exports.view = new MainView();
})(window);
