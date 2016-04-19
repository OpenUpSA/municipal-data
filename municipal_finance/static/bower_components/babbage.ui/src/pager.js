
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
