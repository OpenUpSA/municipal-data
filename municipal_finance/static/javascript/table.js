(function(exports) {
  "use strict";

  // progress indicators
  var spinning = 0;
  function spinnerStart() {
    spinning++;

    // this stops us showing a spinner for cached queries which
    // return very quickly
    _.delay(function() {
      if (spinning > 0) $('#spinner').show();
    }, 200);
  }

  function spinnerStop() {
    spinning--;
    if (spinning === 0) {
      $('#spinner').hide();
    }
  }

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

  var cubes = {};
  var cube = _.extend({}, {
    aggregate: 'amount.sum',
    order: 'item.position_in_return_form:asc',
    drilldown: ['demarcation.code', 'demarcation.label', 'item.code', 'item.label', 'item.return_form_structure', 'item.position_in_return_form'],
  }, cubes[CUBE_NAME] || {});


  /** The filters the user can choose
   */
  var FilterView = Backbone.View.extend({
    el: '.table-controls',
    events: {
      'click .del': 'muniRemoved',
      'click input[name=year]': 'yearChanged',
    },

    initialize: function(opts) {
      this.filters = opts.filters;
      this.filters.on('change', this.render, this);

      this.munis = [];
      this.preload();
    },

    preload: function() {
      var self = this;

      spinnerStart();
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
      }).always(spinnerStop);

      spinnerStart();
      $.get(MUNI_DATA_API + '/cubes/' + CUBE_NAME + '/members/financial_year_end.year', function(data) {
        self.years = _.pluck(data.data, "financial_year_end.year").sort().reverse();
        self.renderYears();
      }).always(spinnerStop);
    },

    render: function() {
      var self = this;

      if (municipalities && !this.$muniChooser) {
        this.renderMunis();
      }

      var munis = _.sortBy(
        _.map(this.filters.get('munis'), function(id) { return municipalities[id]; }),
        'long_name');
      var $list = this.$('.chosen-munis').empty();

      if (munis.length === 0) {
        $list.append('<li>').html('<i>Choose a municipality below.</i>');

      } else {
        _.each(munis, function(muni) {
          $list.append($('<li>')
            .text(muni.long_name)
            .data('id', muni.demarcation_code)
            .prepend('<a href="#" class="del"><i class="fa fa-times-circle"></i></a> ')
          );
        });
      }
    },

    renderMunis: function() {
      function formatMuni(item) {
        if (item.info) {
          return $("<div>" + item.info.name + " (" + item.id + ")<br><i>" + item.info.province_name + "</i></div>");
        } else {
          return item.text;
        }
      }

      var munis = _.map(municipalities, function(muni) {
        return {
          id: muni.demarcation_code,
          text: muni.long_name + " " + muni.demarcation_code,
          info: muni,
        };
      });

      this.$muniChooser = this.$('.muni-chooser').select2({
        data: munis,
        placeholder: "Find a municipality",
        allowClear: true,
        templateResult: formatMuni,
      })
        .on('select2:select', _.bind(this.muniSelected, this));
    },

    renderYears: function() {
      var $chooser = this.$('.year-chooser');

      for (var i = 0; i < this.years.length; i++) {
        var year = this.years[i];
        $chooser.append($('<li><label><input type="radio" name="year" value="' + year + '"> ' + year + '</label></li>'));
      }

      $chooser.find('input:first').prop('checked', true).trigger('click');
    },

    muniSelected: function(e) {
      var munis = this.filters.get('munis');
      var id = e.params.data.id;

      if (id && _.indexOf(munis, id) === -1) {
        munis.push(id);
        this.filters.trigger('change');
      }

      this.$muniChooser.val(null).trigger('change');
    },

    muniRemoved: function(e) {
      e.preventDefault();
      var id = $(e.target).closest('li').data('id');
      this.filters.set('munis', _.without(this.filters.get('munis'), id));
    },

    yearChanged: function(e) {
      this.filters.set('year', Number.parseInt(this.$('input[name=year]:checked').val()));
    },
  });


  /** The data table portion of the page.
   */
  var TableView = Backbone.View.extend({
    el: '#table-view',

    events: {
      'click .scale': 'changeScale',
    },

    initialize: function(opts) {
      this.format = d3_format
        .formatLocale({decimal: ".", thousands: " ", grouping: [3], currency: "R"})
        .format(",d");
      this.scale = 1000;

      this.filters = opts.filters;
      this.filters.on('change', this.render, this);
      this.filters.on('change', this.update, this);

      this.cells = opts.cells;
      this.cells.on('change', this.render, this);

      this.preload();
    },

    preload: function() {
      var self = this;

      // TODO does this work for all cubes?
      spinnerStart();
      $.get(MUNI_DATA_API + '/cubes/' + CUBE_NAME + '/members/item', function(data) {
        self.rowHeadings = data.data;
        self.renderRowHeadings();
      }).always(spinnerStop);
    },

    changeScale: function() {
      var zeroes = this.$('.scale input:checked').attr('value');
      this.scale = Math.pow(10, Number.parseInt(zeroes));
      this.render();
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
      this.cells.set('items', cells);

      _.each(this.filters.get('munis'), function(muni_id) {
        var parts = {
          aggregates: cube.aggregate,
          cut: [],
          drilldown: cube.drilldown,
          order: cube.order,
        };

        // TODO: do this in bulk, rather than 1-by-1
        parts.cut.push('demarcation.code:"' + muni_id + '"');
        parts.cut.push('financial_year_end.year:' + self.filters.get('year'));
        parts.cut.push('financial_period.period:' + self.filters.get('year'));
        parts.cut.push('amount_type.code:AUDA');

        // TODO: paginate
        // make the URL
        url += _.map(parts, function(value, key) {
          if (_.isArray(value)) value = value.join('|');
          return key + '=' + encodeURIComponent(value);
        }).join('&');

        console.log(url);

        spinnerStart();
        $.get(url, function(data) {
          self.cells.set('items', self.cells.get('items').concat(data.cells));
        }).always(spinnerStop);
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
      var self = this;

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
            var cell = cells[row['item.code']];
            if (cell) cell = cell[muni_ids[j]];
            var v = (cell ? cell['amount.sum'] : null);

            tr.insertCell().innerText = v ? self.format(v / this.scale) : "-";
          }
        }
      }
    },
  });


  /** Overall table view on this page
   */
  var MainView = Backbone.View.extend({
    initialize: function() {
      this.filters = new Filters();
      this.cells = new Cells();

      this.filterView = new FilterView({filters: this.filters});
      this.tableView = new TableView({filters: this.filters, cells: this.cells});
    }
  });

  exports.view = new MainView();
})(window);
