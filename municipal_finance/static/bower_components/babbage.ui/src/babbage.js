
ngBabbage.directive('babbage', ['$http', '$rootScope', '$location', 'babbageApi',
    function($http, $rootScope, $location, babbageApi) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      endpoint: '@',
      cube: '@',
      state: '='
    },
    templateUrl: 'babbage-templates/babbage.html',
    controller: ['$scope', function($scope) {
      var self = this,
          modelUpdate = 'babbageModelUpdate',
          state = angular.extend({}, $scope.state || {}, $location.search());

      self.queryModel = {};

      self.init = function(queryModel) {
        self.queryModel = queryModel;
        babbageApi.getModel($scope.endpoint, $scope.cube).then(function(model) {
          $scope.$broadcast(self.modelUpdate, model, state);
        });
      };

      self.subscribe = function(listener) {
        return $scope.$on(self.modelUpdate, listener);
      };

      self.getState = function() {
        return state;
      };

      self.isEmbedded = function() {
        return state.embed == 'true';
      };

      self.setState = function(s) {
        $location.search(s);
      };

      self.getApiUrl = function(endpoint) {
        return babbageApi.getUrl($scope.endpoint, $scope.cube, endpoint);
      };

      self.getDimensionMembers = function(dimension) {
        return babbageApi.getDimensionMembers($scope.endpoint, $scope.cube, dimension);
      };

      self.getSorts = function() {
        var sorts = [],
            order = state.order || '',
            order = asArray(order.split(','));
        for (var i in order) {
          var parts = order[i].split(':'),
              sort = {};
          sort.ref = parts[0],
          sort.direction = parts[1] || null;
          sorts.push(sort);
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
        state.order = self.mergeSorts(sorts);
        self.setState(state);
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
          cut: state.cut || [],
          page: state.page || 0,
          pagesize: state.pagesize || 30,
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
