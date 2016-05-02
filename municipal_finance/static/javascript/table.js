(function(exports) {
  "use strict";

  var Filters = Backbone.Model.extend({});
  var Cells = Backbone.Model.extend({});


  /** The filters the user can choose
   */
  var FilterView = Backbone.View.extend({
    el: '.table-controls',
    events: {
      'change select': 'muniAdded',
    },

    initialize: function(opts) {
      this.filters = opts.filters;
      this.filters.on('change', this.render, this);

      this.munis = [];
      this.preload();
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
        self.filters.trigger('change');
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
      _.each(this.filters.get('munis'), function(id) {
        var muni = self.munis[id];
        var li = $('<li>').text(muni.long_name);
        $holder.append(li);
      });
    },

    muniAdded: function(e) {
      var munis = this.filters.get('munis');
      var id = this.$('.muni-chooser option:selected').attr('value');

      if (id && munis.indexOf(id) === -1) {
        munis.push(id);
        this.filters.trigger('change');
      }
    },
  });


  /** The data table portion of the page.
   */
  var TableView = Backbone.View.extend({
    el: '.table-display',

    initialize: function(opts) {
      this.filters = opts.filters;
      this.filters.on('change', this.update, this);

      this.cells = opts.cells;
      this.cells.on('change', this.render, this);
    },

    /**
     * Update the data!
     */
    update: function() {
      var self = this;
      var url = MUNI_DATA_API + '/cubes/' + CUBE_NAME + '/aggregate?';

      if (this.filters.get('munis').length === 0) {
        this.cells.set({items: [], meta: {}});
        return;
      }

      var parts = {
        // TODO: field to sum over ?
        aggregates: ['amount.sum'],
        // TODO: determine
        drilldown: ['demarcation.code', 'demarcation.label', 'item.code', 'item.label', 'item.return_form_structure'],
        sort: 'item.position_in_return_form',
      };

      // TODO: set filter for municipality
      parts.cut = 'demarcation.code:"' + this.filters.get('munis')[0] + '"';

      // TODO: paginate

      url += _.map(parts, function(value, key) {
        if (_.isArray(value)) value = value.join('|');
        return key + '=' + encodeURIComponent(value);
      }).join('&');

      console.log(url);

      $.get(url, function(data) {
        self.cells.set({items: data.cells, meta: data});
      });
    },

    render: function() {
      // TODO: render correctly
      var cells = this.cells.get('items');
      var table = document.createElement('table');

      for (var i = 0; i < cells.length; i++) {
        var cell = cells[i];
        var tr = table.insertRow();
        var td;

        $(tr).addClass('item-' + cell['item.return_form_structure']);
        
        td = tr.insertCell();
        td.innerText = cell['item.code'];
        td = tr.insertCell();
        td.innerText = cell['item.label'];
      }

      this.$el.empty().append(table);
    },
  });


  /** Overall table view on this page
   */
  var MainView = Backbone.View.extend({
    el: '#table-view',

    initialize: function() {
      this.filters = new Filters({munis: []});
      this.cells = new Cells();

      this.filterView = new FilterView({filters: this.filters});
      this.tableView = new TableView({filters: this.filters, cells: this.cells});
    },
  });

  exports.view = new MainView();
})(window);
