
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
