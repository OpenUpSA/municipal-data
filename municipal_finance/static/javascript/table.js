(function(exports) {
  "use strict";

  var Filters = Backbone.Model.extend({
    // # TODO: init munis
  });

  var Cells = Backbone.Model.extend({});


  /** The data table portion of the page.
   */
  var TableView = Backbone.View.extend({
    el: '.table-display',

    initialize: function() {
      this.model.on('change', this.render);
    },

    render: function() {
      this.$el.html(this.model.length);
    },
  });


  /** The filters the user can choose
   */
  var FilterView = Backbone.View.extend({
    el: '.table-controls',
    events: {
      'change select': 'muniAdded',
    },

    initialize: function() {
      this.munis = [];
      this.preload();

      this.model.on('change', this.render, this);
    },

    preload: function() {
      var self = this;

      $.get(MUNI_DATA_API + '/cubes/municipalities/facts', function(resp) {
        var munis = _.map(resp.data, function(muni) {
          // change municipality.foo to foo
          _.each(_.keys(muni), function(key) {
            if (key.startsWith("municipality.")) {
              muni[key.substring(13)] = muni[key];
              delete muni[key];
            }
          });
          return muni;
        });

        self.munis = _.indexBy(munis, 'demarcation_code');
        self.render();
      });
    },

    render: function() {
      var self = this;

      if (this.$('.muni-chooser option').length === 0) {
        var options = _.map(this.munis, function(muni) {
          return new Option(muni.long_name, muni.demarcation_code);
        });
        $(this.$('.muni-chooser').append(options));
      }

      var $holder = this.$('.chosen-munis').empty();
      _.each(this.model.get('munis'), function(id) {
        var muni = self.munis[id];
        var li = $('<li>').text(muni.long_name);
        $holder.append(li);
      });
    },

    muniAdded: function(e) {
      var munis = this.model.get('munis');
      var id = this.$('.muni-chooser option:selected').attr('value');

      if (id && munis.indexOf(id) === -1) {
        munis.push(id);
        this.model.trigger('change');
      }
    },
  });


  /** Overall table view on this page
   */
  var MainView = Backbone.View.extend({
    el: '#table-view',

    initialize: function() {
      this.filters = new Filters({munis: []});
      this.cells = new Cells();

      this.filterView = new FilterView({model: this.filters});
      this.tableView = new TableView({model: this.cells});
    },

    render: function() {
      // TODO: do stuff
    }
  });

  exports.view = new MainView();
})(window);
