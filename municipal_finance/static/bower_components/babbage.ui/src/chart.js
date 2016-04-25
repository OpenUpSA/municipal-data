
ngBabbage.directive('babbageChart', ['$rootScope', '$http', function($rootScope, $http) {
  return {
    restrict: 'EA',
    require: '^babbage',
    scope: {
      chartType: '@'
    },
    templateUrl: 'babbage-templates/chart.html',
    link: function(scope, element, attrs, babbageCtrl) {
      scope.queryLoaded = false;
      scope.cutoffWarning = false;
      scope.cutoff = 0;

      var getNames = function(model) {
        var names = {};
        for (var ref in model.refs) {
          var concept = model.refs[ref];
          names[ref] = concept.label || concept.name || ref;
        }
        return names;
      };

      var generateColumns = function(cells, category, grouping, value) {
        var columns = [[category]], series = {category: 0};
        for (var i in cells) {
          var cell = cells[i],
              field = grouping ? cell[grouping] : value;
          if (!series[field]) {
            series[field] = columns.push([field]) - 1;
          }
          if (columns[0].indexOf(cell[category]) < 1) {
            columns[0].push(cell[category]);
          }
          var index = columns[0].indexOf(cell[category]);
          columns[series[field]][index] = cell[value];
        }
        var maxLength = Math.max.apply(null, columns.map(function(r) {
          return r.length;
        }));
        for (var i = 1; i < maxLength; i++) {
          for (var j in columns) {
            columns[j][i] = columns[j][i] || 0;
          }
        }
        return columns;
      };

      var query = function(model, state) {
        var category = asArray(state.category)[0],
            grouping = asArray(state.grouping)[0],
            value = asArray(state.value)[0];

        if (!value || !category) {
          babbageCtrl.broadcastInvalidateQuery();
          return;
        }

        var q = babbageCtrl.getQuery();
        q.aggregates = [value];
        q.drilldown = [category];
        if (grouping) {
          q.drilldown.push(grouping);
        }

        var order = [];
        for (var i in q.order) {
          var o = q.order[i];
          if ([value, category].indexOf(o.ref) != -1) {
            order.push(o);
          }
        }
        if (!order.length) {
          order = [{ref: value, direction: 'desc'}];
        }
        if (grouping && order[0] && order[0].ref != grouping) {
          order.unshift({ref: grouping, direction: 'asc'});
        }

        q.order = order;
        q.page = 0;
        q.pagesize = 10000;

        var endpoint = babbageCtrl.getApiUrl('aggregate');
        var dfd = $http.get(endpoint, babbageCtrl.queryParams(q));

        dfd.then(function(res) {
          queryResult(res.data, q, model, state, category, grouping, value);
          babbageCtrl.broadcastQuery(endpoint,
                                     angular.copy(q),
                                     res.data.total_cell_count);
        });
      };

      var queryResult = function(data, q, model, state, category, grouping, value) {
        var wrapper = element.querySelectorAll('.chart-babbage')[0],
            size = babbageCtrl.size(wrapper, function(w) {
              return w * 0.6;
            }),
            colors = ngBabbageGlobals.colorScale.copy(),
            columns = generateColumns(data.cells, category, grouping, value),
            names = getNames(model),
            groups = [], types = {},
            chartType = scope.chartType;

        if (grouping && chartType == 'line') {
          chartType = 'area';
        }

        for (var i in columns) {
          if (i > 0) {
            if (grouping) {
              key = randomKey();
              names[key] = columns[i][0];
              columns[i][0] = key;
              groups.push(key);
            } else {
              groups.push(columns[i][0]);
            }
            types[columns[i][0]] = chartType;
          }
        }

        d3.select(wrapper)
          .style("width", size.width + "px")
          .style("height", size.height + "px");

        var chart = c3.generate({
          bindto: wrapper,
          data: {
              columns: columns,
              names: names,
              color: function(color, d) {
                var c = d.id || d;
                if (chartType == 'bar' && !grouping) {
                  c = d.index;
                };
                return colors(c);
              },
              order: null,
              x: category,
              groups: [groups],
              types: types
          },
          point: {
            show: false
          },
          grid: {
            focus: {
              show: false
            }
          },
          axis: {
              x: {
                  type: 'category',
                  tick: {
                    culling: true,
                    fit: true
                  }
              },
              y : {
                 tick: {
                     format: ngBabbageGlobals.numberFormat,
                     culling: true,
                     fit: true
                 },
                 lines: [{value:0}]
             }
          }
        });

        scope.queryLoaded = true;
        scope.cutoffWarning = data.total_cell_count > q.pagesize;
        scope.cutoff = q.pagesize;
      };

      var unsubscribe = babbageCtrl.subscribe(function(event, model, state) {
        query(model, state);
      });
      scope.$on('$destroy', unsubscribe);

      var queryModel = {
        value: {
          label: 'Value',
          addLabel: 'set height',
          types: ['aggregates'],
          defaults: [],
          sortId: 1,
          multiple: false
        },
        grouping: {
          label: 'Grouping (opt)',
          addLabel: 'select',
          types: ['attributes'],
          defaults: [],
          sortId: 2,
          remove: true,
          multiple: false
        }
      };

      if (scope.chartType == 'line') {
        queryModel.category = {
          label: 'Series',
          addLabel: 'set series',
          types: ['attributes'],
          defaults: [],
          sortId: 0,
          multiple: false
        };
      }

      if (scope.chartType == 'bar') {
        queryModel.category = {
          label: 'Categories',
          addLabel: 'set bars',
          types: ['attributes'],
          defaults: [],
          sortId: 0,
          multiple: false
        };
      }

      babbageCtrl.init(queryModel);
    }
  }
}]);
