var ngBabbage = angular.module('ngBabbage', ['ngBabbage.templates']);

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
