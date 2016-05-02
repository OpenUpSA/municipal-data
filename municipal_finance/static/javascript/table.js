(function(exports) {
  "use strict";

  var Filters = Backbone.Model.extend({
    defaults: {
      munis: [],
    }
  });
  var Cells = Backbone.Model.extend({
    defaults: {
      items: [],
    }
  });
  var municipalities;


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

        municipalities = _.indexBy(munis, 'demarcation_code');
        self.filters.trigger('change');
      });
    },

    render: function() {
      var self = this;

      if (this.$('.muni-chooser option').length === 0) {
        var options = _.map(municipalities, function(muni) {
          return new Option(muni.long_name, muni.demarcation_code);
        });
        $(this.$('.muni-chooser').append(options));
      }

      var $holder = this.$('.chosen-munis').empty();
      _.each(this.filters.get('munis'), function(id) {
        var muni = municipalities[id];
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

      this.preload();
    },

    preload: function() {
      var self = this;
      // TODO does this work for all cubes?
      $.get(MUNI_DATA_API + '/cubes/' + CUBE_NAME + '/members/item', function(data) {
        self.rowHeadings = data.data;
        self.renderRowHeadings();
      });
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

      var cells = [];
      this.cells.set('items', cells, {silent: true});

      _.each(this.filters.get('munis'), function(muni_id) {
        var parts = {
          // TODO: field to sum over ?
          aggregates: ['amount.sum'],
          // TODO: determine
          drilldown: ['demarcation.code', 'demarcation.label', 'item.code', 'item.label', 'item.return_form_structure', 'item.position_in_return_form'],
          order: 'item.position_in_return_form:asc',
        };

        // TODO: set filter for municipality
        parts.cut = 'demarcation.code:"' + muni_id + '"';
        // parts.cut = 'demarcation.code:CPT';

        // TODO: paginate
        // make the URL
        url += _.map(parts, function(value, key) {
          if (_.isArray(value)) value = value.join('|');
          return key + '=' + encodeURIComponent(value);
        }).join('&');

        console.log(url);

        $.get(url, function(data) {
          self.cells.set('items', self.cells.get('items').concat(data.cells));
        });
      });
    },

    render: function() {
      if (this.rowHeadings) {
        this.renderValues();
      }
    },

    renderRowHeadings: function() {
      // render row headings table
      var table = this.$('.row-headings')[0];

      table.insertRow().insertCell().innerHTML = '&nbsp;';

      for (var i = 0; i < this.rowHeadings.length; i++) {
        var item = this.rowHeadings[i];
        var tr = table.insertRow();
        var td;

        $(tr).addClass('item-' + item['item.return_form_structure']);
        
        td = tr.insertCell();
        td.innerText = item['item.code'];
        td = tr.insertCell();
        td.innerText = item['item.label'];
      }
    },

    renderValues: function() {
      var table = this.$('.values').empty()[0];
      var cells = this.cells.get('items');

      // group by code then municipality
      cells = _.groupBy(cells, 'item.code');
      _.each(cells, function(items, code) {
        cells[code] = _.indexBy(items, 'demarcation.code');
      });

      // municipality headings
      var tr = table.insertRow();
      var muni_ids = this.filters.get('munis');
      for (var i = 0; i < muni_ids.length; i++) {
        var th = document.createElement('th');
        th.innerText = municipalities[muni_ids[i]].name;
        tr.appendChild(th);
      }

      // values
      if (!_.isEmpty(cells)) {
        for (i = 0; i < this.rowHeadings.length; i++) {
          var row = this.rowHeadings[i];
          tr = table.insertRow();
          $(tr).addClass('item-' + row['item.return_form_structure']);

          for (var j = 0; j < muni_ids.length; j++) {
            var cell = cells[row['item.code']][muni_ids[j]];
            // TODO: format this number
            var v = (cell ? cell['amount.sum'] : null) || "-";
            tr.insertCell().innerText = v;
          }
        }
      }
    },
  });


  /** Overall table view on this page
   */
  var MainView = Backbone.View.extend({
    el: '#table-view',

    initialize: function() {
      this.filters = new Filters();
      this.cells = new Cells();

      this.filterView = new FilterView({filters: this.filters});
      this.tableView = new TableView({filters: this.filters, cells: this.cells});
    },
  });

  exports.view = new MainView();
})(window);
