
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
