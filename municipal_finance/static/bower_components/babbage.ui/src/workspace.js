
ngBabbage.directive('babbageWorkspace', ['$location', function($location) {
  return {
    restrict: 'EA',
    scope: {
      endpoint: '@',
      cube: '@'
    },
    templateUrl: 'babbage-templates/workspace.html',
    link: function(scope, element, attrs) {
      scope.state = {};
      scope.embedLink = '';
      scope.view = $location.search().view || 'facts';

      scope.setView = function(view) {
        var state = $location.search();
        state.view = view;
        $location.search(state);
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

      prepareEmbed();
    }
  };
}]);
