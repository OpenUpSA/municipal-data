$(() => {
  $.ajax({
    url: '/api/cubes',
  }).done((response) => {
    $('#get-cubes').text(JSON.stringify(response, null, 2));
  });
});

(function (exports) {
  var MainView = Backbone.View.extend({
    el: document,

    events: {
      'click button.accept': 'acceptTOU',
      'click button.decline': 'declineTOU',
    },

    initialize() {
      // show terms of use dialog?
      if (!Cookies.get('tou-ok')) {
        $('#terms-modal').modal();
      } else {
        this.acceptTOU();
      }
    },

    showTOU() {
      $('#terms-modal').modal();
    },

    acceptTOU() {
      Cookies.set('tou-ok', true);
      $('#terms-modal').modal('hide');
      $('#terms-ok').removeClass('hidden');
    },

    declineTOU() {
      Cookies.remove('tou-ok');
      window.location = '/';
    },
  });

  exports.view = new MainView();
}(window));
