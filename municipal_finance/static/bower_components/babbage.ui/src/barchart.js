
ngBabbage.directive('babbageBarchart', ['$rootScope', '$http', function($rootScope, $http) {
  return {
    restrict: 'EA',
    require: '^babbage',
    scope: {
    },
    templateUrl: 'babbage-templates/barchart.html',
    link: function(scope, element, attrs, babbageCtrl) {
      scope.queryLoaded = false;

      var isAggregate = function(aggregates, type) {
        return angular.isDefined(aggregates[type]);
      };

      var getAggregate = function(model, x, y) {
        var aggregate;
        if(isAggregate(model.aggregates, x)) {
          aggregate = x;
        }
        if(isAggregate(model.aggregates, y)) {
          aggregate = y;
        }
        return aggregate;
      };

      var query = function(model, state) {
        var x = asArray(state.x)[0],
            y = asArray(state.y)[0];

        var q = babbageCtrl.getQuery();
        q.aggregates = getAggregate(model, x, y);
        if (!q.aggregates) {
          return;
        }
        var drilldown = (q.aggregates == y) ? x : y;
        q.drilldown = [drilldown];

        var order = [];
        for (var i in q.order) {
          var o = q.order[i];
          if ([x, y].indexOf(o.ref) != -1) {
            order.push(o);
          }
        }
        if (!order.length) {
          order = [{ref: y, direction: 'desc'}];
        }

        q.order = order;
        q.page = 0;
        q.pagesize = 50;

        var dfd = $http.get(babbageCtrl.getApiUrl('aggregate'),
                            babbageCtrl.queryParams(q));
        dfd.then(function(res) {
          queryResult(res.data, q, model, state);
        });
      };

      var slugifyParameter = function(parameter) {
        return parameter.replace(/\./g,"__");
      };

      var typeForParameter = function(model, parameter) {
        return isAggregate(model.aggregates, parameter) ? "Q" : "O";
      };

      var slugifyData = function(data) {
        var dataCells = [];
        data.forEach(function(d) {
          var dCell = {};
          Object.keys(d).forEach(function(key){
              var value = d[key];
              key = slugifyParameter(key);
              dCell[key] = value;
          });
          dataCells.push(dCell);
        });
        return dataCells;
      };

      var widthForChart = function(element) {
        var textWidthDefaultFromVega = 200;
        return parseInt(d3.selectAll(element).node().getBoundingClientRect().width) - textWidthDefaultFromVega;
      };

      var renderChartForSpec = function(shorthand, wrapper) {
        spec = vl.compile(shorthand);
        vg.parse.spec(spec, function(chart) {
          var view = chart({el:wrapper, renderer: "svg"})
            .update();
        });
      };

      var queryResult = function(data, q, model, state) {
        var ySlug, xSlug, shorthand;
        var x = asArray(state.x)[0],
            y = asArray(state.y)[0];
        xSlug = slugifyParameter(x);
        ySlug = slugifyParameter(y);
        shorthand = {
          "data": {
            "values": slugifyData(data.cells)
          },
          "marktype": "bar",
          "encoding": {
            "y": {"type": typeForParameter(model, y), "name": ySlug},
            "x": {"type": typeForParameter(model, x), "name": xSlug},
          },
          "config": {
            "singleWidth": widthForChart(element)
          }
        };
        renderChartForSpec(shorthand, element.querySelectorAll('.barchart-babbage')[0])
        scope.queryLoaded = true;
      };

      var unsubscribe = babbageCtrl.subscribe(function(event, model, state) {
        query(model, state);
      });
      scope.$on('$destroy', unsubscribe);

      babbageCtrl.init({
        y: {
          label: 'Y Axis',
          addLabel: 'set Y axis',
          types: ['attributes', 'aggregates'],
          defaults: [],
          sortId: 0,
          multiple: false
        },
        x: {
          label: 'X Axis',
          addLabel: 'set X axis',
          types: ['attributes', 'aggregates'],
          defaults: [],
          sortId: 1,
          multiple: false
        },
      });
    }
  }
}]);
