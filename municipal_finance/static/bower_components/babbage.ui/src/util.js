
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
