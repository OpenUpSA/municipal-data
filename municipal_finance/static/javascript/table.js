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

  var cube = {
    order: 'item.position_in_return_form:asc',
    drilldown: ['demarcation.code', 'demarcation.label', 'item.code', 'item.label', 'item.return_form_structure', 'item.position_in_return_form'],
    model: CUBES[CUBE_NAME].model,
  };
  cube.aggregates = _.map(cube.model.measures, function(m) { return m.ref + '.sum'; });


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
      var $list = this.$('.chosen-munis').empty();
      var munis = this.filters.get('munis');
      var self = this;

      if (municipalities && !this.$muniChooser) {
        this.renderMunis();
      }

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
      var muni = municipalities[id];

      if (id && _.indexOf(munis, muni) === -1) {
        munis.push(muni);
        this.filters.set('munis', _.sortBy(munis, 'name'));
        this.filters.trigger('change');
      }

      this.$muniChooser.val(null).trigger('change');
    },

    muniRemoved: function(e) {
      e.preventDefault();
      var id = $(e.target).closest('li').data('id');
      this.filters.set('munis', _.without(this.filters.get('munis'), municipalities[id]));
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
      'mouseover .table-display tr': 'rowOver',
      'mouseout .table-display tr': 'rowOut',
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
        // we only care about items that have a label
        self.rowHeadings = _.select(data.data, function(d) { return d['item.label']; });
        self.renderRowHeadings();
        self.render();
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

      var parts = {
        aggregates: cube.aggregates,
        drilldown: cube.drilldown,
        order: cube.order,
        cut: ['financial_period.period:' + self.filters.get('year'),
              // TODO: work out possibilities here based on year
              // eg: https://data.municipalmoney.org.za/api/cubes/incexp/members/amount_type?cut=financial_period:2015
              'amount_type.code:AUDA'],
      };
      var cut = parts.cut;

      _.each(this.filters.get('munis'), function(muni) {
        // duplicate this, we're going to change it
        parts.cut = cut.slice();

        // TODO: do this in bulk, rather than 1-by-1
        parts.cut.push('demarcation.code:"' + muni.demarcation_code + '"');

        // TODO: paginate

        var url = self.makeUrl(parts);
        console.log(url);

        spinnerStart();
        $.get(url, function(data) {
          self.cells.set('items', self.cells.get('items').concat(data.cells));
        }).always(spinnerStop);
      });
    },

    makeUrl: function(parts) {
      var url = MUNI_DATA_API + '/cubes/' + CUBE_NAME + '/aggregate?';
      return url + _.map(parts, function(value, key) {
        if (_.isArray(value)) value = value.join('|');
        return key + '=' + encodeURIComponent(value);
      }).join('&');
    },

    render: function() {
      if (this.rowHeadings) {
        this.renderColHeadings();
        this.renderValues();
      }
    },

    renderRowHeadings: function() {
      // render row headings table
      var table = this.$('.row-headings')[0];

      for (var i = 0; i < (cube.aggregates.length > 1 ? 2 : 1); i++) {
        var spacer = $('<th>').html('&nbsp;').addClass('spacer');
        table.insertRow().appendChild(spacer[0]);
      }

      for (i = 0; i < this.rowHeadings.length; i++) {
        var item = this.rowHeadings[i];
        var tr = table.insertRow();
        var td;

        $(tr).addClass('item-' + item['item.return_form_structure']);
        
        td = tr.insertCell();
        td.innerText = item['item.code'];
        td = tr.insertCell();
        td.innerText = item['item.label'];
        td.setAttribute('title', item['item.label']);
      }
    },

    renderColHeadings: function() {
      var table = this.$('.values').empty()[0];

      // municipality headings
      var tr = table.insertRow();
      var munis = this.filters.get('munis');
      for (var i = 0; i < munis.length; i++) {
        var th = document.createElement('th');
        th.innerText = munis[i].name;
        th.setAttribute('colspan', cube.aggregates.length);
        th.setAttribute('title', munis[i].demarcation_code);
        tr.appendChild(th);
      }

      // aggregate headings
      if (cube.aggregates.length > 1) {
        tr = table.insertRow();

        for (i = 0; i < munis.length; i++) {
          _.each(cube.model.measures, function(measure) {
            var th = document.createElement('th');
            th.innerText = measure.label;
            tr.appendChild(th);
          });
        }
      }
    },

    renderValues: function() {
      var table = this.$('.values')[0];
      var cells = this.cells.get('items');
      var munis = this.filters.get('munis');
      var self = this;

      // group by code then municipality
      cells = _.groupBy(cells, 'item.code');
      _.each(cells, function(items, code) {
        cells[code] = _.indexBy(items, 'demarcation.code');
      });

      // values
      if (!_.isEmpty(cells)) {
        for (var i = 0; i < this.rowHeadings.length; i++) {
          var row = this.rowHeadings[i];
          var tr = table.insertRow();
          $(tr).addClass('item-' + row['item.return_form_structure']);

          for (var j = 0; j < munis.length; j++) {
            var cell = cells[row['item.code']];
            if (cell) cell = cell[munis[j].demarcation_code];

            for (var a = 0; a < cube.aggregates.length; a++) {
              var v = (cell ? cell[cube.aggregates[a]] : null);
              tr.insertCell().innerText = v ? self.format(v / this.scale) : "-";
            }
          }
        }
      }
    },

    rowOver: function(e) {
      var ix = $(e.currentTarget).index();
      this.$('table.row-headings tr:eq(' + ix + '), table.values tr:eq(' + ix + ')')
        .addClass('hover');
    },

    rowOut: function(e) {
      var ix = $(e.currentTarget).index();
      this.$('table.row-headings tr:eq(' + ix + '), table.values tr:eq(' + ix + ')')
        .removeClass('hover');
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
