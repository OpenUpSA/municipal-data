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

  var Filters = Backbone.Model.extend();
  var Cells = Backbone.Model.extend({
    defaults: {
      items: [],
    }
  });
  var State = Backbone.Model.extend({});

  // global municipalities list
  var municipalities;

  // cube settings
  var cube = {
    order: 'item.code:asc',
    drilldown: ['demarcation.code', 'demarcation.label', 'item.code', 'item.label'],
    model: CUBES[CUBE_NAME].model,
  };
  cube.aggregates = _.map(cube.model.measures, function(m) { return m.ref + '.sum'; });
  cube.hasAmountType = !!cube.model.dimensions.amount_type;

  if (cube.model.dimensions.item) {
    if (cube.model.dimensions.item.attributes.return_form_structure) cube.drilldown.push('item.return_form_structure');
    if (cube.model.dimensions.item.attributes.position_in_return_form) {
      cube.order = 'item.position_in_return_form:asc';
    }
  }
  cube.hasFunctions = !!cube.model.dimensions.function;

  // ensure the cube can handle events
  _.extend(cube, Backbone.Events);


  /** The filters the user can choose
   */
  var FilterView = Backbone.View.extend({
    el: '.table-controls',
    events: {
      'click .del': 'muniRemoved',
      'click input[name=year]': 'yearChanged',
      'change select.amount-type-chooser': 'amountTypeChanged',
      'change select.function-chooser': 'functionChanged',
      'click #clear-munis': 'clearMunis',
    },

    initialize: function(opts) {
      this.filters = opts.filters;
      this.filters.on('change', this.render, this);
      this.filters.on('change', this.saveState, this);

      cube.on('change', this.render, this);

      this.state = opts.state;
      this.state.on('change', this.loadState, this);

      this.preload();
      this.loadState();
    },

    loadState: function() {
      // load state from browser history
      this.filters.set({
        municipalities: this.state.get('municipalities') || [],
        year: this.state.get('year'),
        amountType: this.state.get('amountType'),
      });
    },

    saveState: function() {
      // save global state to browser history
      this.state.set({
        municipalities: this.filters.get('municipalities'),
        year: this.filters.get('year'),
        amountType: this.filters.get('amountType'),
      });
    },

    preload: function() {
      this.preloadMunis();
      this.preloadAmountTypes();
      this.preloadFunctions();
    },

    preloadMunis: function() {
      var self = this;

      // preload municipalities
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

        // global municipalities list
        municipalities = _.indexBy(munis, 'demarcation_code');

        // sanity check pre-loaded municipalities
        self.filters.set('municipalities', _.select(self.filters.get('municipalities'), function(id) {
          return !!municipalities[id];
        }), {silent: true});

        // force a change so we re-render
        self.filters.trigger('change');
      }).always(spinnerStop);
    },

    preloadAmountTypes: function() {
      var self = this;

      // preload years and amount types
      var url = '/cubes/' + CUBE_NAME + '/aggregate?aggregates=_count&drilldown=financial_year_end.year';
      if (cube.hasAmountType) url += '|amount_type';

      spinnerStart();
      $.get(MUNI_DATA_API + url, function(data) {
        self.years = _.uniq(_.pluck(data.cells, 'financial_year_end.year')).sort().reverse();
        self.renderYears();

        // sanity check pre-loaded year
        var year = self.filters.get('year');
        year = _.contains(self.years, year) ? year : self.years[0];
        self.filters.set('year', year, {silent: true});

        // amount types per year
        self.amountTypes = {};
        if (cube.hasAmountType) {
          _.each(_.groupBy(data.cells, 'financial_year_end.year'), function(data, year) {
            self.amountTypes[year] = _.sortBy(_.map(data, function(d) {
                return {
                  code: d['amount_type.code'],
                  label: d['amount_type.label'],
                };
              }), 'label');
          });

          // sanity check pre-loaded amount type
          var type = self.filters.get('amountType') || "AUDA";
          if (!type || !_.any(self.amountTypes[year], function(at) { return at.code == type; })) {
            type = self.amountTypes[year][0].code;
          }
          self.filters.set('amountType', type, {silent: true});
        }

        $('.loading').hide();
        self.filters.trigger('change');
      }).always(spinnerStop);
    },

    preloadFunctions: function() {
      if (!cube.hasFunctions) return;

      // preload govt functions
      spinnerStart();
      $.get(MUNI_DATA_API + '/cubes/' + CUBE_NAME + '/members/function?order=function.label', function(resp) {
        cube.functions = _.map(resp.data, function(func) {
          // change municipality.foo to foo
          _.each(_.keys(func), function(key) {
            if (key.startsWith("function.")) {
              func[key.substring(9)] = func[key];
              delete func[key];
            }
          });
          return func;
        });

        cube.trigger('change');
      }).always(spinnerStop);
    },

    render: function() {
      var $list = this.$('.chosen-munis').empty();
      var munis = this.filters.get('municipalities');
      var self = this;

      if (municipalities && !this.$muniChooser) {
        this.renderMunis();
      }

      // show chosen munis
      if (munis.length === 0) {
        $list.append('<li>').html('<i>Choose a municipality above.</i>');
        this.$('.clear-munis').hide();

      } else if (municipalities) {
        this.$('.clear-munis').show();

        _.each(munis, function(muni) {
          muni = municipalities[muni];
          $list.append($('<li>')
            .text(muni.long_name)
            .data('id', muni.demarcation_code)
            .prepend('<a href="#" class="del"><i class="fa fa-times-circle"></i></a> ')
          );
        });
      }

      // ensure year is checked
      var year = (this.filters.get('year') || "").toString();
      this.$('.year-chooser input[name=year]').prop('checked', function() {
        return $(this).val() == year;
      });

      this.renderAmountTypes();

      if (!_.isEmpty(cube.functions) && this.$el.find('.function-chooser option').length == 0) {
        this.renderFunctions();
      }
    },

    renderMunis: function() {
      function formatMuni(item) {
        if (item.info) {
          return $("<div>" + item.info.name + ", " + item.info.province_name + " <i>" + item.id + "</i></div>");
        } else if (item.cat) {
          return $("<div>" + item.text + " <i>Category " + item.cat + "</i></div>");
        } else {
          return $("<div>" + item.text + "</div>");
        }
      }

      // make objects that select2 understands
      var munis = _.map(municipalities, function(muni) {
        return {
          id: muni.demarcation_code,
          text: muni.long_name + " " + muni.demarcation_code,
          info: muni,
        };
      });
      munis = _.sortBy(munis, 'text');

      // add the quick selections
      munis.unshift({
        id: "all",
        text: "All municipalities",
      }, {
        id: "cat-A",
        text: "All metro municipalities",
        cat: "A",
      }, {
        id: "cat-B",
        text: "All local municipalities",
        cat: "B",
      }, {
        id: "cat-C",
        text: "All district municipalities",
        cat: "C",
      });

      this.$muniChooser = this.$('.muni-chooser').select2({
        data: munis,
        placeholder: "Find a municipality",
        allowClear: true,
        templateResult: formatMuni,
      })
        .val(null)
        .trigger('change')
        .on('select2:select', _.bind(this.muniSelected, this));
    },

    renderAmountTypes: function() {
      var $chooser = this.$('.amount-type-chooser'),
          chosen = this.filters.get('amountType'),
          year = this.filters.get('year');

      if (!_.isEmpty(this.amountTypes)) {
        $chooser.closest('section').show();
        $chooser.empty();

        for (var i = 0; i < this.amountTypes[year].length; i++) {
          var at = this.amountTypes[year][i];
          $chooser.append($('<option />').val(at.code).text(at.label));
        }
        $chooser.val(chosen);
      }
    },

    renderFunctions: function() {
      var $chooser = this.$('.function-chooser'),
          chosen = this.filters.get('function') || "all";

      $chooser.closest('section').show();
      $chooser.append($('<option />').val("all").text("All functions"));

      for (var i = 0; i < cube.functions.length; i++) {
        var func = cube.functions[i];
        $chooser.append($('<option />').val(func.code).text(func.label));
      }
      $chooser.val(chosen);
    },

    renderYears: function() {
      var $chooser = this.$('.year-chooser');

      for (var i = 0; i < this.years.length; i++) {
        var year = this.years[i];
        $chooser.append($('<li><label><input type="radio" name="year" value="' + year + '"> ' + year + '</label></li>'));
      }
    },

    muniSelected: function(e) {
      var munis = this.filters.get('municipalities');
      var id = e.params.data.id;

      if (e.params.data.cat) {
        var chosen = _.select(municipalities, function(m) { return m.category == e.params.data.cat; });
        chosen = _.pluck(chosen, 'demarcation_code');
        munis = _.uniq(munis.concat(chosen));

      } else if (id == "all") {
        munis = _.keys(municipalities);

      } else if (id && _.indexOf(munis, id) === -1) {
        // duplicate the array
        munis = munis.concat([id]);
      }

      this.filters.set('municipalities', _.sortBy(munis, function(m) { return municipalities[m].name; }));
      this.filters.trigger('change');
      this.$muniChooser.val(null).trigger('change');
    },

    clearMunis: function(e) {
      e.preventDefault();
      this.filters.set('municipalities', []);
    },

    muniRemoved: function(e) {
      e.preventDefault();
      var id = $(e.target).closest('li').data('id');
      this.filters.set('municipalities', _.without(this.filters.get('municipalities'), id));
    },

    yearChanged: function(e) {
      var year = Number.parseInt(this.$('input[name=year]:checked').val());
      this.filters.set('year', year);

      // sanity check amount type
      var at = this.filters.get('amountType');
      if (!_.isEmpty(this.amountTypes) && !_.any(this.amountTypes[year], function(a) { return a.code == at; })) {
        this.filters.set('amountType', this.amountTypes[year][0].code);
      }
    },

    amountTypeChanged: function(e) {
      this.filters.set('amountType', $(e.target).val());
    },

    functionChanged: function(e) {
      var v = $(e.target).val();

      if (v == "all") {
        this.filters.unset('functions');
      } else {
        this.filters.set('functions', [v]);
      }
    },
  });


  /** The data table portion of the page.
   */
  var TableView = Backbone.View.extend({
    el: '#table-view',

    events: {
      'mouseover .table-display tr': 'rowOver',
      'mouseout .table-display tr': 'rowOut',
      'click .table-display tr': 'rowClick',
    },

    initialize: function(opts) {
      this.format = d3_format
        .formatLocale({decimal: ".", thousands: " ", grouping: [3], currency: "R"})
        .format(",d");
      this.firstRender = true;

      this.filters = opts.filters;
      this.filters.on('change', this.render, this);
      this.filters.on('change', this.update, this);

      this.state = opts.state;

      this.cells = opts.cells;
      this.cells.on('change', this.render, this);

      cube.on('change', this.renderRowHeadings, this);

      this.preload();
    },

    preload: function() {
      var self = this;

      spinnerStart();
      $.get(MUNI_DATA_API + '/cubes/' + CUBE_NAME + '/members/item?order=' + cube.order, function(data) {
        // we only care about items that have a label
        cube.itemHeadings = _.select(data.data, function(d) { return d['item.label']; });
        cube.trigger('change');
        self.render();
      }).always(spinnerStop);
    },

    /**
     * Update the data!
     */
    update: function() {
      var self = this;

      if (this.filters.get('municipalities').length === 0) {
        this.cells.set({items: [], meta: {}});
        return;
      }

      var cells = [];
      this.cells.set('items', cells);

      var parts = {
        aggregates: cube.aggregates,
        drilldown: cube.drilldown,
        cut: ['financial_year_end.year:' + this.filters.get('year')],
      };
      if (this.filters.get('amountType')) {
        parts.cut.push('amount_type.code:' + this.filters.get('amountType'));
      }
      if (cube.model.dimensions.financial_period) {
        parts.cut.push('financial_period.period:' + this.filters.get('year'));
      }
      if (!_.isEmpty(this.filters.get('functions'))) {
        parts.cut.push('function.code:"' + this.filters.get('functions').join('";"') + '"');
        parts.drilldown = ['function.code'].concat(parts.drilldown);
      }

      // duplicate this, we're going to change it
      var cut = parts.cut;
      parts.cut = cut.slice();

      parts.cut.push('demarcation.code:"' + this.filters.get('municipalities').join('";"') + '"');

      // TODO: paginate

      var url = self.makeUrl(parts);
      console.log(url);

      spinnerStart();
      $.get(url, function(data) {
        self.cells.set('items', self.cells.get('items').concat(data.cells));

        // establish download url
        var params = _.clone(parts);
        _.extend(params, {
          page: 1,
          pagesize: data.total_cell_count,
          order: 'demarcation.code:asc,' + cube.order,
        });

        // copy this, we're going to change it
        params.drilldown = params.drilldown.slice();

        // ensure the download has all attributes, except function
        // which we'll deal with later
        _.each(cube.model.dimensions, function(dim, dim_name) {
          if (dim_name != 'function') {
            _.each(dim.attributes, function(attr, attr_name) {
              params.drilldown.unshift(dim_name + '.' + attr_name);
            });
          }
        });

        self.downloadUrl = self.makeUrl(params);
      }).always(spinnerStop);
    },

    makeUrl: function(parts) {
      var url = MUNI_DATA_API + '/cubes/' + CUBE_NAME + '/aggregate?';
      return url + _.map(parts, function(value, key) {
        if (_.isArray(value)) value = value.join('|');
        return key + '=' + encodeURIComponent(value);
      }).join('&');
    },

    render: function() {
      if (cube.itemHeadings && municipalities) {
        this.renderColHeadings();
        this.renderValues();
      }
      this.renderDownloadLinks();
    },

    renderRowHeadings: function() {
      // render row headings table
      var table = this.$('.row-headings')[0];

      for (var i = 0; i < (cube.aggregates.length > 1 ? 2 : 1); i++) {
        var spacer = $('<th>').html('&nbsp;').addClass('spacer');
        table.insertRow().appendChild(spacer[0]);
      }

      for (i = 0; i < (cube.itemHeadings || []).length; i++) {
        var item = cube.itemHeadings[i];
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
      var munis = this.filters.get('municipalities');
      for (var i = 0; i < munis.length; i++) {
        var muni = municipalities[munis[i]];
        var th = document.createElement('th');
        th.innerText = muni.name;
        th.setAttribute('colspan', cube.aggregates.length);
        th.setAttribute('title', muni.demarcation_code);
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
      var munis = this.filters.get('municipalities');
      // highlightable items as a set of codes
      var highlights = _.inject(this.state.get('items') || [], function(s, i) { s[i] = i; return s; }, {});
      // row indexes to highlight
      var toHighlight = [];
      var self = this;

      // group by code then municipality
      cells = _.groupBy(cells, 'item.code');
      _.each(cells, function(items, code) {
        cells[code] = _.indexBy(items, 'demarcation.code');
      });

      // values
      if (!_.isEmpty(cells)) {
        for (var i = 0; i < cube.itemHeadings.length; i++) {
          var row = cube.itemHeadings[i];
          var tr = table.insertRow();
          $(tr).addClass('item-' + row['item.return_form_structure']);

          // highlight?
          if (highlights[row['item.code']]) toHighlight.push(table.rows.length-1);

          for (var j = 0; j < munis.length; j++) {
            var muni = municipalities[munis[j]];
            var cell = cells[row['item.code']];

            if (cell) cell = cell[muni.demarcation_code];

            for (var a = 0; a < cube.aggregates.length; a++) {
              var v = (cell ? cell[cube.aggregates[a]] : null);
              if (v === null) {
                v = "-";
              } else {
                v = self.format(v);
              }

              tr.insertCell().innerText = v;
            }
          }
        }
      }

      // highlighted rows
      for (var h = 0; h < toHighlight.length; h++) {
        var ix = toHighlight[h];
        this.$('table.row-headings tr:eq(' + ix + '), table.values tr:eq(' + ix + ')')
          .addClass('toggled');
      }

      // jump to highlighted row on first render
      if (self.firstRender && toHighlight.length > 0) {
        self.firstRender = false;
        this.$('.table-display').scrollTop(this.$('table.row-headings .toggled').position().top - 50);
      }
    },

    renderDownloadLinks: function() {
      var self = this;

      if (this.downloadUrl && !_.isEmpty(this.filters.get('municipalities'))) {
        this.$('.downloads button').attr('disabled', false);

        // setup urls
        this.$('.downloads .dropdown-menu a').attr('href', function() {
          return self.downloadUrl + '&format=' + $(this).data('format');
        });

      } else {
        this.$('.downloads').attr('disabled', true);
      }
    },

    rowClick: function(e) {
      var ix = $(e.currentTarget).index();
      this.$('table.row-headings tr:eq(' + ix + '), table.values tr:eq(' + ix + ')')
        .toggleClass('toggled');
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
    el: document,
    events: {
      'click button.accept': 'acceptTOU',
      'click button.decline': 'declineTOU',
    },

    initialize: function() {
      this.filters = new Filters();
      this.cells = new Cells();

      this.state = new State();
      this.loadState();
      this.state.on('change', this.saveState, this);

      this.filterView = new FilterView({filters: this.filters, state: this.state});
      this.tableView = new TableView({filters: this.filters, cells: this.cells, state: this.state});

      // show terms of use dialog?
      if (!Cookies.get('tou-ok')) {
        $('#terms-modal').modal();
      } else {
        this.acceptTOU();
      }
    },

    saveState: function() {
      if (history.replaceState) {
        var state = this.state.toJSON();
        var url = {
          year: state.year,
          municipalities: state.municipalities.join(','),
          amountType: state.amountType,
        };

        // make the query string url
        url = _.compact(_.map(url, function(val, key) {
          if (!_.isNaN(val) && (_.isNumber(val) || !_.isEmpty(val))) return key + '=' + encodeURIComponent(val);
        })).join('&');

        history.replaceState({}, document.title, url ? ('?' + url) : "");
      }
    },

    loadState: function() {
      // parse query string
      var params = {};
      var parts = document.location.search.substring(1).split("&");
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i].split('=');
        params[p[0]] = decodeURIComponent(p[1]);
      }

      this.state.set({
        municipalities: (params.municipalities || "").split(","),
        year: Number.parseInt(params.year) || null,
        // highlighted item codes
        items: (params.items || "").split(","),
        amountType: (params.amountType),
      });
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
    },
  });

  exports.view = new MainView();
})(window);
