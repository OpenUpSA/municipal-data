var ngBabbageGlobals = ngBabbageGlobals || {}; ngBabbageGlobals.embedSite = "http://assets.pudo.org/libs/babbage.ui/0.1.7";angular.module('ngBabbage.templates', ['babbage-templates/babbage.html', 'babbage-templates/chart.html', 'babbage-templates/crosstab.html', 'babbage-templates/facts.html', 'babbage-templates/pager.html', 'babbage-templates/panel.html', 'babbage-templates/sankey.html', 'babbage-templates/treemap.html', 'babbage-templates/workspace.html']);

angular.module("babbage-templates/babbage.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/babbage.html",
    "<div class=\"babbage-frame\" ng-transclude></div>");
}]);

angular.module("babbage-templates/chart.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/chart.html",
    "<div class=\"table-babbage\" ng-hide=\"queryLoaded\"><div class=\"alert alert-info\"><strong>You have not selected any data.</strong> Please choose the configuration for your chart.</div></div><div class=\"alert alert-warning\" ng-show=\"cutoffWarning\"><strong>Too many categories.</strong> There are more than {{cutoff}} items in the selected drilldown.</div><div class=\"chart-babbage\"><svg></svg></div>");
}]);

angular.module("babbage-templates/crosstab.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/crosstab.html",
    "<div class=\"table-babbage\" ng-show=\"rows.length\"><table class=\"table table-bordered table-condensed\"><thead><tr ng-repeat=\"x in columns[0]\"><th ng-repeat=\"r in rows[0]\"></th><th ng-repeat=\"c in columns\">{{c[$parent.$index]}}</th></tr></thead><tbody><tr ng-repeat=\"row in rows\"><th ng-repeat=\"r in row\">{{r}}</th><td ng-repeat=\"val in table[$index] track by $index\" class=\"numeric\">{{val | numeric}}</td></tr></tbody></table></div><div class=\"table-babbage\" ng-hide=\"rows.length || !queryLoaded\"><div class=\"alert alert-info\"><strong>You have not selected any data.</strong> Please choose a set of rows and columns to generate a cross-table.</div></div>");
}]);

angular.module("babbage-templates/facts.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/facts.html",
    "<div class=\"table-babbage\" ng-show=\"data\"><table class=\"table table-bordered table-striped table-condensed\"><thead><tr><th ng-repeat-start=\"c in columns\" class=\"title\">{{ c.header }} <span class=\"sublabel\" ng-hide=\"c.hide\">{{ c.label }}</span></th><th ng-repeat-end class=\"operations\" ng-switch=\"getSort(c.ref).direction\"><span ng-switch-when=\"desc\" ng-click=\"pushSort(c.ref, 'asc')\" class=\"ng-link\"><i class=\"fa fa-sort-desc\"></i></span> <span ng-switch-when=\"asc\" ng-click=\"pushSort(c.ref, 'desc')\" class=\"ng-link\"><i class=\"fa fa-sort-asc\"></i></span> <span ng-switch-default ng-click=\"pushSort(c.ref, 'desc')\" class=\"ng-link\"><i class=\"fa fa-sort\"></i></span></th></tr></thead><tbody><tr ng-repeat=\"row in data\"><td ng-repeat=\"c in columns\" ng-class=\"{'numeric': c.numeric}\" class=\"simple\" colspan=\"2\"><span ng-if=\"c.numeric\">{{ row[c.ref] | numeric }}</span> <span ng-if=\"!c.numeric\">{{ row[c.ref] }}</span></td></tr></tbody></table></div><babbage-pager context=\"pagerCtx\"></babbage-pager>");
}]);

angular.module("babbage-templates/pager.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/pager.html",
    "<ul ng-show=\"showPager\" class=\"pagination pagination-sm\"><li ng-class=\"{'disabled': !hasPrev}\"><a class=\"ng-link\" ng-click=\"setPage(current - 1)\">&laquo;</a></li><li ng-repeat=\"page in pages\" ng-class=\"{'active': page.current}\"><a class=\"ng-link\" ng-click=\"setPage(page.page)\">{{page.page}}</a></li><li ng-class=\"{'disabled': !hasNext}\"><a class=\"ng-link\" ng-click=\"setPage(current + 1)\">&raquo;</a></li></ul>");
}]);

angular.module("babbage-templates/panel.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/panel.html",
    "<div class=\"panel panel-default\" ng-repeat=\"axis in axes\"><div class=\"panel-heading\"><strong>{{axis.label}}</strong><div class=\"btn-group\" dropdown ng-show=\"axis.available.length\">&mdash; <a dropdown-toggle class=\"ng-link\">{{axis.addLabel}}</a><ul class=\"dropdown-menu\" role=\"menu\"><li ng-repeat=\"opt in axis.available\"><a ng-click=\"add(axis, opt.ref)\"><strong>{{opt.label}}</strong> {{opt.subLabel}}</a></li></ul></div></div><table class=\"table\"><tr ng-repeat=\"opt in axis.active\"><td colspan=\"2\"><div class=\"pull-right\"><span ng-switch=\"getSort(opt.ref).direction\"><a ng-switch-when=\"desc\" ng-click=\"pushSort(opt.ref, 'asc')\" class=\"ng-link ng-icon\"><i class=\"fa fa-sort-amount-desc\"></i></a> <a ng-switch-when=\"asc\" ng-click=\"pushSort(opt.ref, 'desc')\" class=\"ng-link ng-icon\"><i class=\"fa fa-sort-amount-asc\"></i></a> <a ng-switch-default ng-click=\"pushSort(opt.ref, 'desc')\" class=\"ng-link ng-icon\"><i class=\"fa fa-sort-amount-desc\"></i></a></span> <a ng-click=\"remove(axis, opt.ref)\" ng-show=\"axis.remove\" class=\"ng-link ng-icon\"><i class=\"fa fa-times\"></i></a></div><strong>{{opt.label}}</strong> {{opt.subLabel}}</td></tr></table></div><div class=\"panel panel-default\"><div class=\"panel-heading\"><strong>Filters</strong><div class=\"btn-group\" dropdown ng-show=\"filterAttributes.length\">&mdash; <a dropdown-toggle class=\"ng-link\">add filter</a><ul class=\"dropdown-menu\" role=\"menu\"><li ng-repeat=\"attr in filterAttributes\"><a ng-click=\"addFilter(attr)\"><strong>{{attr.label}}</strong> {{attr.subLabel}}</a></li></ul></div></div><table class=\"table table-panel\"><tbody ng-repeat=\"filter in filters\"><tr><td colspan=\"2\"><strong>{{filter.attr.label}}</strong> {{filter.attr.subLabel}}</td><td width=\"1%\"><span class=\"pull-right\"><a ng-click=\"removeFilter(filter)\" class=\"ng-link\"><i class=\"fa fa-times\"></i></a></span></td></tr><tr class=\"adjoined\"><td width=\"1%\" class=\"middle\">is</td><td width=\"95%\"><ui-select ng-model=\"filter.value\" disable-search=\"false\" on-select=\"setFilter(filter, $item, $model)\"><ui-select-match placeholder=\"Pick one...\">{{$select.selected}}</ui-select-match><ui-select-choices repeat=\"v as v in filter.values | filter: $select.search track by $index\"><div ng-bind=\"v\"></div></ui-select-choices></ui-select></td><td class=\"middle\"></td></tr></tbody></table></div><div class=\"btn\" ng-show=\"csvLink != null\"><a class=\"btn btn-default\" href=\"{{ csvLink }}\">Download CSV</a></div>");
}]);

angular.module("babbage-templates/sankey.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/sankey.html",
    "<div class=\"table-babbage\" ng-hide=\"queryLoaded\"><div class=\"alert alert-info\"><strong>You have not selected any data.</strong> Please choose a breakdown for both sides of the flow diagram.</div></div><div class=\"alert alert-warning\" ng-show=\"cutoffWarning\"><strong>Too many links.</strong> The source and target you have selected have many different links, only the {{cutoff}} biggest are shown.</div><div class=\"sankey-babbage\"></div>");
}]);

angular.module("babbage-templates/treemap.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/treemap.html",
    "<div class=\"table-babbage\" ng-hide=\"queryLoaded\"><div class=\"alert alert-info\"><strong>You have not selected any data.</strong> Please choose a breakdown for your treemap.</div></div><div class=\"alert alert-warning\" ng-show=\"cutoffWarning\"><strong>Too many tiles.</strong> The breakdown you have selected contains many different categories, only the {{cutoff}} biggest are shown.</div><div class=\"treemap-babbage\"></div>");
}]);

angular.module("babbage-templates/workspace.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/workspace.html",
    "<babbage endpoint=\"{{endpoint}}\" cube=\"{{cube}}\" state=\"state\" update=\"update(state)\"><div class=\"row\"><div class=\"col-md-12\"><div class=\"pull-right\"><div class=\"btn-group spaced\" role=\"group\"><a class=\"btn btn-default\" ng-class=\"{'active': view == 'facts'}\" ng-click=\"setView('facts')\"><i class=\"fa fa-table\"></i> Items</a> <a class=\"btn btn-default\" ng-class=\"{'active': view == 'crosstab'}\" ng-click=\"setView('crosstab')\"><i class=\"fa fa-cubes\"></i> Pivot table</a> <a class=\"btn btn-default\" ng-class=\"{'active': view == 'barchart'}\" ng-click=\"setView('barchart')\"><i class=\"fa fa-bar-chart\"></i> Bar chart</a> <a class=\"btn btn-default\" ng-class=\"{'active': view == 'linechart'}\" ng-click=\"setView('linechart')\"><i class=\"fa fa-line-chart\"></i> Line chart</a> <a class=\"btn btn-default\" ng-class=\"{'active': view == 'treemap'}\" ng-click=\"setView('treemap')\"><i class=\"fa fa-th-large\"></i> Treemap</a> <a class=\"btn btn-default\" ng-class=\"{'active': view == 'sankey'}\" ng-click=\"setView('sankey')\"><i class=\"fa fa-random\"></i> Flow</a></div></div></div></div><div class=\"row\"><div class=\"col-md-9\"><div ng-if=\"view == 'crosstab'\"><babbage-crosstab></babbage-crosstab></div><div ng-if=\"view == 'facts'\"><babbage-facts></babbage-facts></div><div ng-if=\"view == 'treemap'\"><babbage-treemap></babbage-treemap></div><div ng-if=\"view == 'barchart'\"><babbage-chart chart-type=\"bar\"></babbage-chart></div><div ng-if=\"view == 'linechart'\"><babbage-chart chart-type=\"line\"></babbage-chart></div><div ng-if=\"view == 'sankey'\"><babbage-sankey></babbage-sankey></div></div><div class=\"col-md-3\"><babbage-panel></babbage-panel><div class=\"embed-link\"><p class=\"help-block\">Embed this view into another website:</p><div class=\"input-group\"><span class=\"input-group-addon\"><i class=\"fa fa-external-link-square\"></i></span> <input type=\"text\" class=\"form-control\" readonly=\"readonly\" value=\"<style>.babbage-embed{position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;} .babbage-embed iframe{position:absolute;top:0;left:0;width:100%;height:100%;}</style><div class='babbage-embed'><iframe src='{{embedLink}}' frameborder='0' allowfullscreen></iframe></div>\"></div></div></div></div></babbage>");
}]);
;var ngBabbage = angular.module('ngBabbage', ['ngBabbage.templates']);

var ngBabbageGlobals = ngBabbageGlobals || {};
ngBabbageGlobals.numberFormat = d3.format("0,000");
ngBabbageGlobals.categoryColors = [
    "#CF3D1E", "#F15623", "#F68B1F", "#FFC60B", "#DFCE21",
    "#BCD631", "#95C93D", "#48B85C", "#00833D", "#00B48D",
    "#60C4B1", "#27C4F4", "#478DCB", "#3E67B1", "#4251A3", "#59449B",
    "#6E3F7C", "#6A246D", "#8A4873", "#EB0080", "#EF58A0", "#C05A89"
    ];
ngBabbageGlobals.colorScale = d3.scale.ordinal().range(ngBabbageGlobals.categoryColors);

if(!ngBabbageGlobals.embedSite) {
  var url = window.location.href.split('#')[0],
      lastSlash = url.lastIndexOf('/'),
      lastSlash = lastSlash == -1 ? url.length : lastSlash;
  ngBabbageGlobals.embedSite = url.slice(0, lastSlash);
}
ngBabbageGlobals.embedLink = ngBabbageGlobals.embedSite + '/embed.html';


ngBabbage.filter('numeric', function() {
  return function(val) {
    var fval = parseFloat(val)
    if (isNaN(fval)) {
      return '-';
    }
    return ngBabbageGlobals.numberFormat(Math.round(fval));
  };
});
;
ngBabbage.factory('babbageApi', ['$http', '$q', 'slugifyFilter', function($http, $q, slugifyFilter) {
  var cache = {};

  var getUrl = function(endpoint, cube, path) {
    var api = endpoint.slice(),
        api = api.endsWith('/') ? api.slice(0, api.length - 1) : api,
        api = api + '/cubes/' + cube + '/' + path;
    return api;
  };

  var getCached = function(url) {
    if (!angular.isDefined(cache[url])) {
      cache[url] = $http.get(url);
    }
    return cache[url];
  };

  var getModel = function(endpoint, cube) {
    return getCached(getUrl(endpoint, cube, 'model')).then(function(res) {
      var model = res.data.model;
      model.refs = {};
      model.refKeys = {};
      model.refLabels = {};

      for (var i in model.measures) {
        var measure = model.measures[i];
        measure.numeric = true;
        measure.hideLabel = true;
        model.refs[measure.ref] = measure;
      }

      for (var i in model.aggregates) {
        var agg = model.aggregates[i];
        agg.numeric = true;
        agg.hideLabel = true;
        model.refs[agg.ref] = agg;
      }

      for (var di in model.dimensions) {
        var dim = model.dimensions[di];
        for (var ai in dim.attributes) {
          var attr = dim.attributes[ai],
              nested = attr.ref.indexOf('.') != -1;
          attr.dimension = dim;
          attr.hideLabel = slugifyFilter(attr.label) == slugifyFilter(dim.label);
          model.refs[attr.ref] = attr;
          model.refKeys[attr.ref] = nested ? dim.name + '.' + dim.key_attribute : attr.ref;
          model.refLabels[attr.ref] = nested ? dim.name + '.' + dim.label_attribute : attr.ref;
        }
      }
      return model;
    });
  };

  var getDimensionMembers = function(endpoint, cube, dimension) {
    return getCached(getUrl(endpoint, cube, 'members/' + dimension));
  };

  var flush = function() {
    cache = {};
  };

  return {
    getUrl: getUrl,
    getModel: getModel,
    getDimensionMembers: getDimensionMembers,
    flush: flush
  };
}]);
;
ngBabbage.directive('babbage', ['$http', '$rootScope', '$location', 'babbageApi',
    function($http, $rootScope, $location, babbageApi) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      endpoint: '@',
      cube: '@',
      state: '=',
      update: '&'
    },
    templateUrl: 'babbage-templates/babbage.html',
    controller: ['$scope', function($scope) {
      var self = this;
      self.queryModel = null;

      self.init = function(queryModel) {
        self.queryModel = queryModel;
        self.update();
      };

      self.update = function() {
        if (self.queryModel) {
          babbageApi.getModel($scope.endpoint, $scope.cube).then(function(model) {
            $scope.$broadcast('babbageUpdate', model, $scope.state);
          });
        }
      }

      self.subscribe = function(listener) {
        return $scope.$on('babbageUpdate', listener);
      };

      self.subscribeQuery = function(listener) {
        return $scope.$on('babbageQuery', listener);
      };

      self.broadcastQuery = function(endpoint, params, item_count) {
        $scope.$broadcast('babbageQuery', endpoint, params, item_count);
      };

      self.subscribeInvalidateQuery = function(listener) {
        return $scope.$on('babbageInvalidateQuery', listener);
      };

      self.broadcastInvalidateQuery = function() {
        $scope.$broadcast('babbageInvalidateQuery');
      };

      self.getState = function() {
        return $scope.state;
      };

      self.isEmbedded = function() {
        return $scope.state.embed == 'true';
      };

      self.setState = function(s) {
        $scope.state = s;
        self.update();
        $scope.update(s);
      };

      self.getApiUrl = function(endpoint) {
        return babbageApi.getUrl($scope.endpoint, $scope.cube, endpoint);
      };

      self.getDimensionMembers = function(dimension) {
        return babbageApi.getDimensionMembers($scope.endpoint, $scope.cube, dimension);
      };

      self.size = function(element, height) {
        if (self.isEmbedded()) {
            return {
              width: document.documentElement.clientWidth,
              height: document.documentElement.clientHeight
            }
        }
        return {
          width: element.clientWidth,
          height: height(element.clientWidth, element.clientHeight)
        }
      };

      self.getSorts = function() {
        var sorts = [],
            order = $scope.state.order || '',
            order = asArray(order.split(','));
        for (var i in order) {
          var parts = order[i].split(':'),
              sort = {};
          sort.ref = parts[0];
          sort.direction = parts[1] || null;
          if (sort.ref.length) {
              sorts.push(sort);
          }
        }
        return sorts;
      };

      self.getSort = function(ref) {
        var sorts = self.getSorts();
        for (var i in sorts) {
          if (sorts[i].ref == ref) {
            return sorts[i];
          }
        }
        return {ref: ref};
      };

      self.pushSort = function(ref, direction) {
        var sorts = self.getSorts().filter(function(s) {
          return s.ref != ref;
        });
        sorts.unshift({ref: ref, direction: direction});
        $scope.state.order = self.mergeSorts(sorts);
        self.setState($scope.state);
      };

      self.removeSorts = function(ref) {
        var sorts = self.getSorts().filter(function(s) {
          return s.ref != ref;
        });
        return self.mergeSorts(sorts);
      };

      self.mergeSorts = function(order) {
        var sorts = [];
        order = asArray(order);
        for (var i in order) {
          var o = order[i];
          if (angular.isObject(o) && o.ref.length) {
            o.direction = o.direction || 'asc';
            o = o.ref + ':' + o.direction;
            sorts.push(o);
          }
        }
        return sorts.join(',');
      };

      self.getQuery = function() {
        var q = {
          drilldown: [],
          aggregates: [],
          cut: $scope.state.cut || [],
          page: $scope.state.page || 0,
          pagesize: $scope.state.pagesize || 30,
          order: self.getSorts()
        };
        return q;
      };

      self.queryParams = function(q) {
        q.order = self.mergeSorts(q.order);

        // join arguments and remove empty arguments
        for (var k in q) {
          if (angular.isArray(q[k])) {
            if (['order', 'fields'].indexOf(k) != -1) {
              q[k] = q[k].join(',');
            } else {
              q[k] = q[k].join('|');
            }
          }
          q[k] = q[k] + '';
          if (!q[k].length) {
            delete q[k];
          }
        }
        return {params: q};
      }
    }]
  };
}]);
;
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
;var VAL_KEY = '@@@@',
    POS_KEY = '!@!@'

ngBabbage.directive('babbageCrosstab', ['$rootScope', '$http', function($rootScope, $http) {
  return {
  restrict: 'EA',
  require: '^babbage',
  scope: {
    drilldown: '='
  },
  templateUrl: 'babbage-templates/crosstab.html',
  link: function(scope, element, attrs, babbageCtrl) {
    scope.queryLoaded = false;
    scope.columns = [];
    scope.rows = [];
    scope.table = [];

    var query = function(model, state) {
      state.rows = asArray(state.rows);
      state.columns = asArray(state.columns);
      state.aggregates = asArray(state.aggregates);
      // TODO: handle a case in which both sets contain the same
      // ref.

      var q = babbageCtrl.getQuery();
      q.aggregates = q.aggregates.concat(state.aggregates);
      if (!q.aggregates.length) {
        q.aggregates = defaultAggregates(model);
      }
      q.drilldown = q.drilldown.concat(state.rows);
      q.drilldown = q.drilldown.concat(state.columns);
      q.page = 0;
      q.pagesize = q.pagesize * 10000;

      q.order = asArray(q.order);
      var drilldowns = state.rows.concat(state.columns),
          refs = drilldowns.concat(q.aggregates);
      for (var i in drilldowns) {
        var dd = drilldowns[i];
        if (!babbageCtrl.getSort(dd).direction) {
          if (q.order.indexOf(dd) == -1) {
            q.order.push({ref: dd});
          }
        }
      }
      var order = [];
      for (var i in q.order) {
        var o = q.order[i];
        if (refs.indexOf(o.ref) != -1) {
          order.push(o);
        }
      }
      q.order = order;

      var endpoint = babbageCtrl.getApiUrl('aggregate');
      var dfd = $http.get(endpoint, babbageCtrl.queryParams(q));

      dfd.then(function(res) {
        queryResult(res.data, q, model, state);
        babbageCtrl.broadcastQuery(endpoint,
                                   angular.copy(q),
                                   res.data.total_cell_count);
      });
    };

    var queryResult = function(data, q, model, state) {
      state.rows = asArray(state.rows);
      state.columns = asArray(state.columns);

      var aggregates = data.aggregates.map(function(agg) {
        return model.aggregates[agg];
      });

      // following code inspired by:
      // https://github.com/DataBrewery/babbage/blob/master/babbage/formatters.py#L218
      var matrix = {}, table = [],
          row_headers = [], column_headers = [],
          row_keys = [], column_keys = [];

      for (var i in data.cells) {
        var pickValue = function(k) { return cell[k]; },
            pickRefs = function(k) { return cell[model.refKeys[k]] + cell[k]; };

        var cell = data.cells[i],
            row_values = state.rows.map(pickValue),
            row_set = state.rows.map(pickRefs).join(VAL_KEY),
            all_column_values = state.columns.map(pickValue),
            all_column_set = state.columns.map(pickRefs);

        for (var k in aggregates) {
          var agg = aggregates[k],
              label = agg.label || agg.name,
              column_values = all_column_values.concat([label]);
              column_set = all_column_set.concat([label]).join(VAL_KEY)

          if (row_keys.indexOf(row_set) == -1) {
            row_keys.push(row_set);
            row_values.key = row_set;
            row_headers.push(row_values);
          }

          if (column_keys.indexOf(column_set) == -1) {
            column_keys.push(column_set);
            column_headers.push(column_values);
          }

          var key = [row_set, column_set].join(POS_KEY);
          matrix[key] = cell[agg.ref];
        }
      }

      for (var i in row_keys) {
        var row_key = row_keys[i];
        var row = [];
        for (var j in column_keys) {
          var column_key = column_keys[j];
          var key = [row_key, column_key].join(POS_KEY);
          row.push(matrix[key] || data.aggregates.map(function(a) { return undefined; }));
        }
        table.push(row);
      }

      scope.rows = row_headers;
      scope.columns = column_headers;
      scope.table = table;
      scope.queryLoaded = true;
    };


    var unsubscribe = babbageCtrl.subscribe(function(event, model, state) {
      query(model, state);
    });
    scope.$on('$destroy', unsubscribe);

    var defaultAggregates = function(model) {
      var aggs = [];
      for (var i in model.aggregates) {
        var agg = model.aggregates[i];
        aggs.push(agg.ref);
      }
      return aggs;
    };

    // console.log('crosstab init');
    babbageCtrl.init({
      columns: {
        label: 'Columns',
        addLabel: 'add column',
        types: ['attributes'],
        defaults: [],
        sortId: 0,
        multiple: true
      },
      rows: {
        label: 'Rows',
        addLabel: 'add row',
        types: ['attributes'],
        defaults: [],
        sortId: 1,
        multiple: true
      },
      aggregates: {
        label: 'Values',
        addLabel: 'add value',
        types: ['aggregates'],
        defaults: defaultAggregates,
        sortId: 2,
        multiple: true
      },

    });
  }
  };
}]);
;
ngBabbage.directive('babbageFacts', ['$rootScope', '$http', '$q', function($rootScope, $http, $q) {
  return {
  restrict: 'EA',
  require: '^babbage',
  scope: {
    drilldown: '='
  },
  templateUrl: 'babbage-templates/facts.html',
  link: function(scope, element, attrs, babbageCtrl) {
    scope.page = 0;
    scope.data = [];
    scope.columns = [];
    scope.pagerCtx = {};
    scope.getSort = babbageCtrl.getSort;
    scope.pushSort = babbageCtrl.pushSort;

    var query = function(model, state) {
      var q = babbageCtrl.getQuery();
      q.fields = asArray(state.fields);
      if (q.fields.length == 0) {
        q.fields = defaultFields(model);
      }

      var order = [];
      for (var i in q.order) {
        var o = q.order[i];
        if (q.fields.indexOf(o.ref) != -1) {
          order.push(o);
        }
      }
      q.order = order;

      var aq = angular.copy(q);
      aq.drilldown = aq.fields = [];
      aq.page = 0;
      var endpoint = babbageCtrl.getApiUrl('facts');
      var dfd = $http.get(endpoint, babbageCtrl.queryParams(q));

      dfd.then(function(res) {
        queryResult(res.data, q, state, model);
        babbageCtrl.broadcastQuery(endpoint,
                                   angular.copy(q),
                                   res.data.total_fact_count);
      });
    };

    var queryResult = function(data, q, state, model) {
      if (!data.data.length) {
        scope.columns = [];
        scope.data = [];
        scope.pagerCtx = {};
        return;
      };

      var columns = [],
          prev = null,
          prev_idx = 0;

      for (var i in data.fields) {
        var ref = data.fields[i],
            column = model.refs[ref],
            header = column.dimension ? column.dimension : column;

        if (prev && header.name == prev) {
          columns[prev_idx].span += 1;
          column.span = 0;
        } else {
          column.span = 1;
          column.label = column.label || column.name;
          column.header = header.label || header.name;
          column.hide = column.hideLabel;
          prev = header.name;
          prev_idx = columns.length;
        }
        columns.push(column);
      }
      scope.columns = columns;
      scope.data = data.data;
      scope.pagerCtx = {
        page: q.page,
        pagesize: q.pagesize,
        total: data.total_fact_count
      }
    };

    var defaultFields = function(model) {
      var defaults = [];
      for (var i in model.measures) {
        var mea = model.measures[i];
        defaults.push(mea.ref);
      }
      for (var i in model.dimensions) {
        var dim = model.dimensions[i];
        for (var k in dim.attributes) {
          var attr = dim.attributes[k];
          if (k == dim.label_attribute) {
            defaults.push(attr.ref);
          }
        }
      }
      return defaults;
    };

    var unsubscribe = babbageCtrl.subscribe(function(event, model, state) {
      query(model, state);
    });
    scope.$on('$destroy', unsubscribe);

    // console.log('facts init');
    babbageCtrl.init({
      fields: {
        label: 'Columns',
        addLabel: 'add column',
        types: ['attributes', 'measures'],
        defaults: defaultFields,
        sortId: 0,
        multiple: true
      }
    });
  }
  };
}]);
;
ngBabbage.directive('babbagePager', ['$timeout', '$location', function ($timeout, $location) {
  return {
    restrict: 'E',
    require: '^babbage',
    scope: {
      'context': '='
    },
    templateUrl: 'babbage-templates/pager.html',
    link: function (scope, element, attrs, babbageCtrl) {
      scope.showPager = false;
      scope.hasPrev = false;
      scope.hasNext = false;
      scope.pages = [];
      scope.current = 1;
      scope.num = 1;

      scope.$watch('context', function(e) {
        if (!scope.context || scope.context.total <= scope.context.pagesize) {
          return;
        }
        scope.current = parseInt(scope.context.page, 10) || 1;
        scope.num = Math.ceil(scope.context.total / scope.context.pagesize);
        var pages = [],
          num = scope.num,
          range = 3,
          low = scope.current - range,
          high = scope.current + range;

        if (low < 1) {
          low = 1;
          high = Math.min((2*range)+1, num);
        }
        if (high > num) {
          high = num;
          low = Math.max(1, num - (2*range)+1);
        }

        for (var page = low; page <= high; page++) {
          // var offset = (page - 1) * scope.context.pagesize;
          pages.push({
            page: page,
            current: page == scope.current,
            //offset: offset
          });
        }
        scope.hasPrev = scope.current > 1;
        scope.hasNext = scope.current < num;
        scope.showPager = num > 1;
        scope.pages = pages;
      });

      scope.setPage = function(page) {
        if (page >= 1 && page <= scope.num) {
          var state = babbageCtrl.getState();
          state.page = page;
          babbageCtrl.setState(state);
        }
      };
    }
  };
}]);
;
ngBabbage.directive('babbagePanel', ['$rootScope', 'slugifyFilter', function($rootScope, slugifyFilter) {
  return {
    restrict: 'EA',
    require: '^babbage',
    scope: {
    },
    templateUrl: 'babbage-templates/panel.html',
    link: function($scope, $element, attrs, babbageCtrl) {
      var model = null;
      $scope.state = {};
      $scope.axes = [];
      $scope.filterAttributes = [];
      $scope.filters = [];
      $scope.getSort = babbageCtrl.getSort;
      $scope.pushSort = babbageCtrl.pushSort;
      $scope.embedLink = null;
      $scope.csvLink = null;

      var update = function() {
        babbageCtrl.setState($scope.state);
      };

      $scope.add = function(axis, ref) {
        if (axis.selected.indexOf(ref) == -1) {
          if (axis.multiple) {
            axis.selected.push(ref);
          } else {
            if (axis.selected.length) {
              $scope.state.order = babbageCtrl.removeSorts(axis.selected[0]);
            }
            axis.selected = [ref];
          }
          $scope.state[axis.name] = axis.selected;
          update();
        }
      };

      $scope.remove = function(axis, ref) {
        var i = axis.selected.indexOf(ref);
        if (i != -1) {
          axis.selected.splice(i, 1);
          $scope.state[axis.name] = axis.selected;
          $scope.state.order = babbageCtrl.removeSorts(ref);
          update();
        }
      };

      var makeOptions = function() {
        var options = [];
        for (var di in model.dimensions) {
          var dim = model.dimensions[di];
          for (var ai in dim.attributes) {
            var attr = angular.copy(dim.attributes[ai]);
            attr.dimension = dim;
            attr.type = 'attributes';
            if (slugifyFilter(dim.label) != slugifyFilter(attr.label)) {
              attr.subLabel = '' + attr.label;
            }
            attr.sortKey = '0' + dim.label + attr.label;
            attr.label = dim.label;
            options.push(attr);
          }
        }

        for (var ai in model.aggregates) {
          var agg = model.aggregates[ai];
          agg.type = 'aggregates';
          agg.sortKey = '1' + ai;
          options.push(agg);
        }

        for (var mi in model.measures) {
          var mea = model.measures[mi];
          mea.type = 'measures';
          mea.sortKey = '2' + mi;
          options.push(mea);
        }

        return options;
      }

      var sortOptions = function(a, b) {
        return a.label.localeCompare(b.label);
      }

      var makeAxes = function(state, options) {
        var axes = [];
        if (!babbageCtrl.queryModel) return [];

        for (var name in babbageCtrl.queryModel) {
          var axis = babbageCtrl.queryModel[name];
          axis.name = name;
          if (!angular.isDefined(axis.remove)) {
            axis.remove = axis.multiple;
          }
          axis.sortId = axis.sortId || 1;
          axis.available = [];
          axis.active = [];

          axis.selected = asArray(state[name]);
          if (!axis.selected.length) {
            if (angular.isFunction(axis.defaults)) {
              axis.selected = axis.defaults(model);
            } else {
              axis.selected = asArray(axis.defaults);
            }
          }
          axis.available = axis.available.sort(sortOptions);
          axis.active = axis.active.sort(sortOptions);

          for (var i in options) {
            var opt = options[i];
            if (axis.selected.indexOf(opt.ref) != -1) {
              axis.active.push(opt);
            } else if (axis.types.indexOf(opt.type) != -1) {
              axis.available.push(opt);
            }
          }
          axes.push(axis);
        }

        return axes.sort(function(a, b) {
          return a.sortId - b.sortId;
        });
      };

      var makeFilterAttributes = function(options) {
        var filters = [];
        for (var i in options) {
          var opt = options[i];
          if (opt.type == 'attributes' && opt.dimension.cardinality_class != 'high') {
            if (opt.dimension.label_ref == opt.ref) {
              filters.push(opt);
            }
          }
        }
        return filters.sort(sortOptions);
      };

      var getAttributeByRef = function(ref) {
        for (var i in $scope.filterAttributes) {
          var attr = $scope.filterAttributes[i];
          if (attr.ref == ref) {
            return attr;
          }
        }
      };

      var loadFilters = function(state) {
        var cuts = asArray(state.cut);
        for (var i in cuts) {
          var cut = cuts[i];
          if (cut.indexOf(':') != -1) {
            var ref = cut.split(':', 1)[0],
                values = cut.slice(ref.length + 1).split(';');
            for (var j in values) {
              $scope.addFilter(getAttributeByRef(ref), values[j]);
            }
          }
        }
      };

      $scope.addFilter = function(attr, value) {
        babbageCtrl.getDimensionMembers(attr.ref).then(function(res) {
          $scope.filters.push({
            ref: attr.ref,
            attr: attr,
            value: value,
            values: res.data.data.map(function(e) {
              return e[attr.ref];
            })
          });
        });
      };

      $scope.removeFilter = function(filter) {
        var idx = $scope.filters.indexOf(filter);
        if (idx != -1) {
          $scope.filters.splice(idx, 1);
          $scope.updateFilters();
        }
      };

      $scope.setFilter = function(filter, item, value) {
        $scope.updateFilters();
      };

      $scope.updateFilters = function() {
        var filters = {};
        for (var i in $scope.filters) {
          var f = $scope.filters[i];
          if (angular.isUndefined(filters[f.ref])) {
            filters[f.ref] = [];
          }
          filters[f.ref].push(f.value);
        }
        var cuts = [];
        for (var ref in filters) {
          var values = filters[ref],
              value = values.join(';')
              cut = ref + ':' + value;
          cuts.push(cut);
        }
        $scope.state.cut = cuts;
        update();
      };

      var unsubscribe = babbageCtrl.subscribe(function(event, mdl, state) {
        model = mdl;
        $scope.state = state;

        var options = makeOptions();
        $scope.axes = makeAxes(state, options);
        $scope.filterAttributes = makeFilterAttributes(options);
        $scope.filters = [];
        loadFilters(state);

      });
      $scope.$on('$destroy', unsubscribe);

      var unsubscribeQuery = babbageCtrl.subscribeQuery(
        function(event, endpoint, params, itemCount) {
          params['format'] = 'csv';
          params['page'] = 1;
          params['pagesize'] = itemCount;
          url = endpoint + '?' + jQuery.param(params);
          $scope.csvLink = url;
        });
      $scope.$on('$destroy', unsubscribeQuery);

      var unsubscribeInvalidateQuery = babbageCtrl.subscribeInvalidateQuery(
        function(event) {
          $scope.csvLink = null;
        });
      $scope.$on('$destroy', unsubscribeInvalidateQuery);
    }
  };
}]);
;
ngBabbage.directive('babbageSankey', ['$rootScope', '$http', '$document', function($rootScope, $http, $document) {
  return {
  restrict: 'EA',
  require: '^babbage',
  scope: {
    drilldown: '='
  },
  templateUrl: 'babbage-templates/sankey.html',
  link: function(scope, element, attrs, babbageCtrl) {
    var unit = 15,
        margin = {top: unit / 2, right: 1, bottom: 6, left: 1},
        svg = null, group = null;

    scope.queryLoaded = false;
    scope.cutoffWarning = false;
    scope.cutoff = 0;

    var query = function(model, state) {
      var source = asArray(state.source)[0],
          target = asArray(state.target)[0]
          aggregate = asArray(state.aggregate)[0],
          aggregate = aggregate ? [aggregate] : defaultAggregate(model);

      var q = babbageCtrl.getQuery();
      q.aggregates = aggregate;
      if (!source || !target) {
        babbageCtrl.broadcastInvalidateQuery();
        return;
      }
      q.drilldown = [source, target];

      q.order = [
        {
          ref: aggregate,
          direction: 'desc'
        },
        {
          ref: source,
          direction: 'asc'
        },
        {
          ref: target,
          direction: 'asc'
        }
      ];
      q.page = 0;
      q.pagesize = 2000;

      scope.queryLoaded = true;
      scope.cutoffWarning = false;
      var endpoint = babbageCtrl.getApiUrl('aggregate');
      var dfd = $http.get(endpoint, babbageCtrl.queryParams(q));

      var wrapper = element.querySelectorAll('.sankey-babbage')[0],
          size = babbageCtrl.size(wrapper, function(w) { return w * 0.6; });

      unit = Math.max(400, size.height) / 20;

      if (!svg) {
          svg = d3.select(wrapper).append("svg");
          group = svg.append("g")
              .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      }

      dfd.then(function(res) {
        queryResult(size, res.data, q, model, state);
        babbageCtrl.broadcastQuery(endpoint,
                                   angular.copy(q),
                                   res.data.total_cell_count);
      });
    };

    var queryResult = function(size, data, q, model, state) {
      var sourceRef = asArray(state.source)[0],
          targetRef = asArray(state.target)[0]
          aggregateRef = asArray(state.aggregate)[0],
          aggregateRef = aggregateRef ? [aggregateRef] : defaultAggregate(model),
          size.height = data.cells.length * unit;

      svg.attr("height", size.height + margin.top + margin.bottom);
      svg.attr("width", size.width);

      var graph = {nodes: [], links: []},
          objs = {};

      var sourceScale = ngBabbageGlobals.colorScale.copy(),
          targetScale = d3.scale.ordinal().range(['#ddd', '#ccc', '#eee', '#bbb']);

      data.cells.forEach(function(cell) {
        var sourceId = cell[sourceRef],
            targetId = cell[targetRef],
            link = {
              //value: Math.sqrt(cell[aggregateRef]),
              value: cell[aggregateRef],
              number: ngBabbageGlobals.numberFormat(cell[aggregateRef])
            };

        if (link.value == 0 || !sourceId || !targetId) {
          return;
        }
        sourceId = 'source-' + sourceRef + sourceId;
        targetId = 'target-' + targetRef + targetId;

        if (!objs[sourceId]) {
          var label = cell[model.refLabels[sourceRef]];
          graph.nodes.push({
            name: label,
            color: sourceScale(sourceId)
          });
          objs[sourceId] = {idx: graph.nodes.length - 1};
        }
        link.source = objs[sourceId].idx;

        if (!objs[targetId]) {
          var label = cell[model.refLabels[targetRef]];
          graph.nodes.push({
            name: label,
            color: targetScale(targetId)
          });
          objs[targetId] = {
            idx: graph.nodes.length - 1
          };
        }
        link.target = objs[targetId].idx;
        graph.links.push(link);
      });

      var sankey = d3.sankey()
         .nodeWidth(unit)
         .nodePadding(unit * 0.6)
         .size([size.width, size.height]);

      var path = sankey.link();

      sankey
        .nodes(graph.nodes)
        .links(graph.links)
        .layout(32);

      group.selectAll('g').remove();

      var link = group.append("g").selectAll(".link")
          .data(graph.links)
        .enter().append("path")
          .attr("class", "link")
          .attr("d", path)
          .style("stroke-width", function(d) {
            return Math.max(1, d.dy);
          })
          .style("stroke", function(d) {
            return d.source.color;
          })
          .sort(function(a, b) { return b.dy - a.dy; });

      link.append("title")
          .text(function(d) { return d.source.name + " → " + d.target.name + "\n" + d.number; });

      var node = group.append("g").selectAll(".node")
          .data(graph.nodes)
        .enter().append("g")
          .attr("class", "node")
          .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

      node.append("rect")
          .attr("height", function(d) { return d.dy; })
          .attr("width", sankey.nodeWidth())
          .style("fill", function(d) { return d.color; })
          //.style("stroke", function(d) { return d3.rgb(d.color).darker(1); })
          .style("stroke", function(d) { return d.color; })
        .append("title")
          .text(function(d) { return d.name });

      node.append("text")
          .attr("x", -6)
          .attr("y", function(d) { return d.dy / 2; })
          .attr("dy", ".35em")
          .attr("text-anchor", "end")
          .attr("transform", null)
          .text(function(d) { return d.name; })
        .filter(function(d) { return d.x < size.width / 2; })
          .attr("x", 6 + sankey.nodeWidth())
          .attr("text-anchor", "start");

      scope.cutoffWarning = data.total_cell_count > q.pagesize;
      scope.cutoff = q.pagesize;
    };

    var unsubscribe = babbageCtrl.subscribe(function(event, model, state) {
      query(model, state);
    });
    scope.$on('$destroy', unsubscribe);

    var defaultAggregate = function(model) {
      for (var i in model.aggregates) {
        var agg = model.aggregates[i];
        if (agg.measure) {
          return [agg.ref];
        }
      }
      return [];
    };

    babbageCtrl.init({
      source: {
        label: 'Source',
        addLabel: 'set left side',
        types: ['attributes'],
        defaults: [],
        sortId: 0,
        multiple: false
      },
      target: {
        label: 'Target',
        addLabel: 'set right side',
        types: ['attributes'],
        defaults: [],
        sortId: 1,
        multiple: false
      },
      aggregate: {
        label: 'Width',
        addLabel: 'set width',
        types: ['aggregates'],
        defaults: defaultAggregate,
        sortId: 2,
        multiple: false
      },

    });
  }
  };
}]);
;
ngBabbage.directive('babbageTreemap', ['$rootScope', '$http', '$document', function($rootScope, $http, $document) {
  return {
  restrict: 'EA',
  require: '^babbage',
  scope: {
    drilldown: '='
  },
  templateUrl: 'babbage-templates/treemap.html',
  link: function(scope, element, attrs, babbageCtrl) {
    var treemap = null,
        div = null;

    scope.queryLoaded = false;
    scope.cutoffWarning = false;

    var query = function(model, state) {
      var tile = asArray(state.tile)[0],
          area = asArray(state.area)[0],
          area = area ? [area] : defaultArea(model);

      var q = babbageCtrl.getQuery();
      q.aggregates = area;
      if (!tile) {
        babbageCtrl.broadcastInvalidateQuery();
        return;
      }
      q.drilldown = [tile];

      var order = [];
      for (var i in q.order) {
        var o = q.order[i];
        if ([tile, area].indexOf(o.ref) != -1) {
          order.push(o);
        }
      }
      if (!order.length) {
        order = [{ref: area, direction: 'desc'}];
      }

      q.order = order;
      q.page = 0;
      q.pagesize = 50;

      scope.cutoffWarning = false;
      scope.queryLoaded = true;
      var endpoint = babbageCtrl.getApiUrl('aggregate');
      var dfd = $http.get(endpoint, babbageCtrl.queryParams(q));

      var wrapper = element.querySelectorAll('.treemap-babbage')[0],
          size = babbageCtrl.size(wrapper, function(w) { return w * 0.6; });

      treemap = d3.layout.treemap()
        .size([size.width, size.height])
        .sticky(true)
        .sort(function(a, b) { return a[area] - b[area]; })
        .value(function(d) { return d[area]; });

      d3.select(wrapper).select("div").remove();
      div = d3.select(wrapper).append("div")
        .style("position", "relative")
        .style("width", size.width + "px")
        .style("height", size.height + "px");

      dfd.then(function(res) {
        queryResult(res.data, q, model, state);
        babbageCtrl.broadcastQuery(endpoint,
                                   angular.copy(q),
                                   res.data.total_cell_count);
      });
    };

    var queryResult = function(data, q, model, state) {
      var tileRef = asArray(state.tile)[0],
          areaRef = asArray(state.area)[0],
          areaRef = areaRef ? [areaRef] : defaultArea(model);

      var root = {
        children: []
      };

      for (var i in data.cells) {
        var cell = data.cells[i];
        cell._area_fmt = ngBabbageGlobals.numberFormat(Math.round(cell[areaRef]));
        cell._name = cell[tileRef];
        cell._color = ngBabbageGlobals.colorScale(i);
        cell._percentage = cell[areaRef] / Math.max(data.summary[areaRef], 1);
        root.children.push(cell);
      };

      var node = div.datum(root).selectAll(".node")
          .data(treemap.nodes)
        .enter().append("a")
          .attr("href", function(d){ return d.href; })
          .attr("class", "node")
          .call(positionNode)
          .style("background", '#fff')
          .html(function(d) {
            if (d._percentage < 0.02) {
              return '';
            }
            return d.children ? null : '<span class="amount">' + d._area_fmt + '</span>' + d._name;
          })
          .on("mouseover", function(d) {
            d3.select(this).transition().duration(200)
              .style({'background': d3.rgb(d._color).darker() });
          })
          .on("mouseout", function(d) {
            d3.select(this).transition().duration(500)
              .style({'background': d._color});
          })
          .transition()
          .duration(500)
          .delay(function(d, i) { return Math.min(i * 30, 1500); })
          .style("background", function(d) { return d._color; });

      scope.cutoffWarning = data.total_cell_count > q.pagesize;
      scope.cutoff = q.pagesize;
    };

    function positionNode() {
      this.style("left", function(d) { return d.x + "px"; })
          .style("top", function(d) { return d.y + "px"; })
          .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
          .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
    };


    var unsubscribe = babbageCtrl.subscribe(function(event, model, state) {
      query(model, state);
    });
    scope.$on('$destroy', unsubscribe);

    var defaultArea = function(model) {
      for (var i in model.aggregates) {
        var agg = model.aggregates[i];
        if (agg.measure) {
          return [agg.ref];
        }
      }
      return [];
    };

    babbageCtrl.init({
      tile: {
        label: 'Tiles',
        addLabel: 'set breakdown',
        types: ['attributes'],
        defaults: [],
        sortId: 0,
        multiple: false
      },
      area: {
        label: 'Area',
        addLabel: 'set area',
        types: ['aggregates'],
        defaults: defaultArea,
        sortId: 1,
        multiple: false
      },
    });
  }
  };
}]);
;
function asArray(obj) {
  objs = obj ? obj : [];
  return angular.isArray(objs) ? objs : [objs];
}

function randomKey() {
  return 'X' + Math.random().toString(36).substring(7);
}

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/endsWith
// suggested polyfill for safari & IE
if (!String.prototype.endsWith) {
  String.prototype.endsWith = function(searchString, position) {
      var subjectString = this.toString();
      if (position === undefined || position > subjectString.length) {
        position = subjectString.length;
      }
      position -= searchString.length;
      var lastIndex = subjectString.indexOf(searchString, position);
      return lastIndex !== -1 && lastIndex === position;
  };
}
;
ngBabbage.directive('babbageWorkspace', ['$location', function($location) {
  return {
    restrict: 'EA',
    scope: {
      endpoint: '@',
      cube: '@'
    },
    templateUrl: 'babbage-templates/workspace.html',
    link: function(scope, element, attrs) {
      scope.state = null;
      scope.embedLink = null;

      scope.setView = function(view) {
        scope.view = view;
        scope.state.view = view;
        scope.update(scope.state);
      };

      scope.update = function(state) {
        scope.state = state;
        scope.view = scope.state.view || 'facts';
        $location.search(state);
        prepareEmbed();
      };

      var prepareEmbed = function() {
        var qs = [],
            opts = angular.extend({}, $location.search(), {
              view: scope.view,
              endpoint: scope.endpoint,
              cube: scope.cube,
              embed: true
            });
        for (var name in opts) {
          var values = asArray(opts[name]);
          for (var i in values) {
            var val = encodeURIComponent(values[i]);
            qs.push(name + '=' + val);
          }
        }
        scope.embedLink = ngBabbageGlobals.embedLink + '#/?' + qs.join('&');
      };

      scope.update($location.search());
    }
  };
}]);
