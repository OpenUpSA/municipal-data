angular.module('ngBabbage.templates', ['babbage-templates/babbage.html', 'babbage-templates/barchart.html', 'babbage-templates/crosstab.html', 'babbage-templates/facts.html', 'babbage-templates/pager.html', 'babbage-templates/panel.html', 'babbage-templates/sankey.html', 'babbage-templates/treemap.html', 'babbage-templates/workspace.html']);

angular.module("babbage-templates/babbage.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/babbage.html",
    "<div class=\"babbage-frame\" ng-transclude>\n" +
    "</div>\n" +
    "");
}]);

angular.module("babbage-templates/barchart.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/barchart.html",
    "<div class=\"table-babbage\" ng-hide=\"queryLoaded\">\n" +
    "  <div class=\"alert alert-info\">\n" +
    "    <strong>You have not selected any data.</strong> Please choose a breakdown for\n" +
    "    your treemap.\n" +
    "  </div>\n" +
    "</div>\n" +
    "<div class=\"barchart-babbage\">\n" +
    "");
}]);

angular.module("babbage-templates/crosstab.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/crosstab.html",
    "<div class=\"table-babbage\" ng-show=\"rows.length\">\n" +
    "  <table class=\"table table-bordered table-condensed\">\n" +
    "    <thead>\n" +
    "      <tr ng-repeat=\"x in columns[0]\">\n" +
    "        <th ng-repeat=\"r in rows[0]\"></th>\n" +
    "        <th ng-repeat=\"c in columns\">\n" +
    "          {{c[$parent.$index]}}\n" +
    "        </th>\n" +
    "      </tr>\n" +
    "    </thead>\n" +
    "    <tbody>\n" +
    "      <tr ng-repeat=\"row in rows\">\n" +
    "        <th ng-repeat=\"r in row\">\n" +
    "          {{r}}\n" +
    "        </th>\n" +
    "        <td ng-repeat=\"val in table[$index] track by $index\" class=\"numeric\">\n" +
    "          {{val | numeric}}\n" +
    "        </td>\n" +
    "      </tr>\n" +
    "    </tbody>\n" +
    "  </table>\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"table-babbage\" ng-hide=\"rows.length || !queryLoaded\">\n" +
    "  <div class=\"alert alert-info\">\n" +
    "    <strong>You have not selected any data.</strong> Please choose a set of rows\n" +
    "    and columns to generate a cross-table.\n" +
    "  </div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("babbage-templates/facts.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/facts.html",
    "<div class=\"table-babbage\" ng-show=\"data\">\n" +
    "  <table class=\"table table-bordered table-striped table-condensed\">\n" +
    "    <thead>\n" +
    "      <tr>\n" +
    "        <th ng-repeat-start=\"c in columns\" class=\"title\">\n" +
    "          {{ c.header }}\n" +
    "          <span class=\"sublabel\" ng-hide=\"c.hide\">{{ c.label }}</span>\n" +
    "        </th>\n" +
    "        <th ng-repeat-end class=\"operations\" ng-switch=\"getSort(c.ref).direction\">\n" +
    "          <span ng-switch-when=\"desc\" ng-click=\"pushSort(c.ref, 'asc')\" class=\"ng-link\">\n" +
    "            <i class=\"fa fa-sort-desc\"></i>\n" +
    "          </span>\n" +
    "          <span ng-switch-when=\"asc\" ng-click=\"pushSort(c.ref, 'desc')\" class=\"ng-link\">\n" +
    "            <i class=\"fa fa-sort-asc\"></i>\n" +
    "          </span>\n" +
    "          <span ng-switch-default ng-click=\"pushSort(c.ref, 'desc')\" class=\"ng-link\">\n" +
    "            <i class=\"fa fa-sort\"></i>\n" +
    "          </span>\n" +
    "        </th>\n" +
    "      </tr>\n" +
    "    </thead>\n" +
    "    <tbody>\n" +
    "      <tr ng-repeat=\"row in data\">\n" +
    "        <td ng-repeat=\"c in columns\" ng-class=\"{'numeric': c.numeric}\" class=\"simple\"\n" +
    "          colspan=\"2\">\n" +
    "          <span ng-if=\"c.numeric\">\n" +
    "            {{ row[c.ref] | numeric }}\n" +
    "          </span>\n" +
    "          <span ng-if=\"!c.numeric\">\n" +
    "            {{ row[c.ref] }}\n" +
    "          </span>\n" +
    "        </td>\n" +
    "      </tr>\n" +
    "    </tbody>\n" +
    "  </table>\n" +
    "</div>\n" +
    "<babbage-pager context=\"pagerCtx\"></babbage-pager>\n" +
    "");
}]);

angular.module("babbage-templates/pager.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/pager.html",
    "<ul ng-show=\"showPager\" class=\"pagination pagination-sm\">\n" +
    "  <li ng-class=\"{'disabled': !hasPrev}\">\n" +
    "    <a class=\"ng-link\" ng-click=\"setPage(current - 1)\">&laquo;</a>\n" +
    "  </li>\n" +
    "  <li ng-repeat=\"page in pages\" ng-class=\"{'active': page.current}\">\n" +
    "    <a class=\"ng-link\" ng-click=\"setPage(page.page)\">{{page.page + 1}}</a>\n" +
    "  </li>\n" +
    "  <li ng-class=\"{'disabled': !hasNext}\">\n" +
    "    <a class=\"ng-link\" ng-click=\"setPage(current + 1)\">&raquo;</a>\n" +
    "  </li>\n" +
    "</ul>\n" +
    "");
}]);

angular.module("babbage-templates/panel.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/panel.html",
    "<div class=\"panel panel-default\" ng-repeat=\"axis in axes\">\n" +
    "  <div class=\"panel-heading\">\n" +
    "    <strong>{{axis.label}}</strong>\n" +
    "\n" +
    "    <div class=\"btn-group\" dropdown ng-show=\"axis.available.length\">\n" +
    "      &mdash;\n" +
    "      <a dropdown-toggle class=\"ng-link\">{{axis.addLabel}}</a>\n" +
    "      <ul class=\"dropdown-menu\" role=\"menu\">\n" +
    "        <li ng-repeat=\"opt in axis.available\">\n" +
    "          <a ng-click=\"add(axis, opt.ref)\">\n" +
    "            <strong>{{opt.label}}</strong>\n" +
    "            {{opt.subLabel}}\n" +
    "          </a>\n" +
    "        </li>\n" +
    "      </ul>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <table class=\"table\">\n" +
    "    <tr ng-repeat=\"opt in axis.active\">\n" +
    "      <td colspan=\"2\">\n" +
    "        <div class=\"pull-right\">\n" +
    "          <span ng-switch=\"getSort(opt.ref).direction\">\n" +
    "            <a ng-switch-when=\"desc\" ng-click=\"pushSort(opt.ref, 'asc')\" class=\"ng-link ng-icon\">\n" +
    "              <i class=\"fa fa-sort-amount-desc\"></i></a>\n" +
    "            <a ng-switch-when=\"asc\" ng-click=\"pushSort(opt.ref, 'desc')\" class=\"ng-link ng-icon\">\n" +
    "              <i class=\"fa fa-sort-amount-asc\"></i></a>\n" +
    "            <a ng-switch-default ng-click=\"pushSort(opt.ref, 'desc')\" class=\"ng-link ng-icon\">\n" +
    "              <i class=\"fa fa-sort-amount-desc\"></i></a>\n" +
    "          </span>\n" +
    "          <a ng-click=\"remove(axis, opt.ref)\" ng-show=\"axis.multiple\" class=\"ng-link ng-icon\">\n" +
    "            <i class=\"fa fa-times\"></i></a>\n" +
    "        </div>\n" +
    "        <strong>{{opt.label}}</strong>\n" +
    "        {{opt.subLabel}}\n" +
    "      </td>\n" +
    "    </tr>\n" +
    "  </table>\n" +
    "</div>\n" +
    "\n" +
    "\n" +
    "<div class=\"panel panel-default\">\n" +
    "  <div class=\"panel-heading\">\n" +
    "    <strong>Filters</strong>\n" +
    "\n" +
    "    <div class=\"btn-group\" dropdown ng-show=\"filterAttributes.length\">\n" +
    "      &mdash;\n" +
    "      <a dropdown-toggle class=\"ng-link\">add filter</a>\n" +
    "      <ul class=\"dropdown-menu\" role=\"menu\">\n" +
    "        <li ng-repeat=\"attr in filterAttributes\">\n" +
    "          <a ng-click=\"addFilter(attr)\">\n" +
    "            <strong>{{attr.label}}</strong>\n" +
    "            {{attr.subLabel}}\n" +
    "          </a>\n" +
    "        </li>\n" +
    "      </ul>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <table class=\"table table-panel\">\n" +
    "    <tbody ng-repeat=\"filter in filters\">\n" +
    "      <tr>\n" +
    "        <td colspan=\"2\">\n" +
    "          <strong>{{filter.attr.label}}</strong>\n" +
    "          {{filter.attr.subLabel}}\n" +
    "        </td>\n" +
    "        <td width=\"1%\">\n" +
    "          <span class=\"pull-right\">\n" +
    "            <a ng-click=\"removeFilter(filter)\" class=\"ng-link\">\n" +
    "              <i class=\"fa fa-times\"></i>\n" +
    "            </a>\n" +
    "          </span>\n" +
    "        </td>\n" +
    "      </tr>\n" +
    "      <tr class=\"adjoined\">\n" +
    "        <td width=\"1%\" class=\"middle\">\n" +
    "          is\n" +
    "        </td>\n" +
    "        <td width=\"95%\">\n" +
    "          <ui-select ng-model=\"filter.value\" disable-search=\"false\" on-select=\"setFilter(filter, $item, $model)\">\n" +
    "            <ui-select-match placeholder=\"Pick one...\">{{$select.selected}}</ui-select-match>\n" +
    "            <ui-select-choices repeat=\"v as v in filter.values | filter: $select.search track by $index\">\n" +
    "               <div ng-bind=\"v\"></div>\n" +
    "            </ui-select-choices>\n" +
    "          </ui-select>\n" +
    "        </td>\n" +
    "        <td class=\"middle\">\n" +
    "        </td>\n" +
    "      </tr>\n" +
    "    </tbody>\n" +
    "  </table>\n" +
    "</div>\n" +
    "");
}]);

angular.module("babbage-templates/sankey.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/sankey.html",
    "<div class=\"table-babbage\" ng-hide=\"queryLoaded\">\n" +
    "  <div class=\"alert alert-info\">\n" +
    "    <strong>You have not selected any data.</strong> Please choose a breakdown for\n" +
    "    both sides of the flow diagram.\n" +
    "  </div>\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"alert alert-warning\" ng-show=\"cutoffWarning\">\n" +
    "  <strong>Too many links.</strong> The source and target you have selected\n" +
    "  have many different links, only the {{cutoff}} biggest are shown.\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"sankey-babbage\"></div>\n" +
    "");
}]);

angular.module("babbage-templates/treemap.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/treemap.html",
    "<div class=\"table-babbage\" ng-hide=\"queryLoaded\">\n" +
    "  <div class=\"alert alert-info\">\n" +
    "    <strong>You have not selected any data.</strong> Please choose a breakdown for\n" +
    "    your treemap.\n" +
    "  </div>\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"alert alert-warning\" ng-show=\"cutoffWarning\">\n" +
    "  <strong>Too many tiles.</strong> The breakdown you have selected contains many\n" +
    "  different categories, only the {{cutoff}} biggest are shown.\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"treemap-babbage\"></div>\n" +
    "");
}]);

angular.module("babbage-templates/workspace.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("babbage-templates/workspace.html",
    "<babbage endpoint=\"{{endpoint}}\" cube=\"{{cube}}\" state=\"state\">\n" +
    "  <div class=\"row\">\n" +
    "    <div class=\"col-md-12\">\n" +
    "      <div class=\"pull-right\">\n" +
    "        <div class=\"btn-group spaced\" role=\"group\">\n" +
    "          <a class=\"btn btn-default\"\n" +
    "            ng-class=\"{'active': view == 'facts'}\"\n" +
    "            ng-click=\"setView('facts')\">\n" +
    "            <i class=\"fa fa-table\"></i> Items\n" +
    "          </a>\n" +
    "          <a class=\"btn btn-default\"\n" +
    "            ng-class=\"{'active': view == 'crosstab'}\"\n" +
    "            ng-click=\"setView('crosstab')\">\n" +
    "            <i class=\"fa fa-cubes\"></i> Pivot table\n" +
    "          </a>\n" +
    "          <a class=\"btn btn-default\"\n" +
    "            ng-class=\"{'active': view == 'barchart'}\"\n" +
    "            ng-click=\"setView('barchart')\">\n" +
    "            <i class=\"fa fa-bar-chart\"></i> Bar chart\n" +
    "          </a>\n" +
    "          <a class=\"btn btn-default\"\n" +
    "            ng-class=\"{'active': view == 'treemap'}\"\n" +
    "            ng-click=\"setView('treemap')\">\n" +
    "            <i class=\"fa fa-th-large\"></i> Treemap\n" +
    "          </a>\n" +
    "          <a class=\"btn btn-default\"\n" +
    "            ng-class=\"{'active': view == 'sankey'}\"\n" +
    "            ng-click=\"setView('sankey')\">\n" +
    "            <i class=\"fa fa-random\"></i> Flow\n" +
    "          </a>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"row\">\n" +
    "    <div class=\"col-md-9\">\n" +
    "      <div ng-if=\"view == 'crosstab'\">\n" +
    "        <babbage-crosstab></babbage-crosstab>\n" +
    "      </div>\n" +
    "      <div ng-if=\"view == 'facts'\">\n" +
    "        <babbage-facts></babbage-facts>\n" +
    "      </div>\n" +
    "      <div ng-if=\"view == 'treemap'\">\n" +
    "        <babbage-treemap></babbage-treemap>\n" +
    "      </div>\n" +
    "      <div ng-if=\"view == 'barchart'\">\n" +
    "        <babbage-barchart></babbage-barchart>\n" +
    "      </div>\n" +
    "      <div ng-if=\"view == 'sankey'\">\n" +
    "        <babbage-sankey></babbage-sankey>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "    <div class=\"col-md-3\">\n" +
    "      <babbage-panel></babbage-panel>\n" +
    "\n" +
    "      <div class=\"embed-link\">\n" +
    "        <p class=\"help-block\">Embed this view into another website:</p>\n" +
    "        <div class=\"input-group\">\n" +
    "          <span class=\"input-group-addon\">\n" +
    "            <i class=\"fa fa-external-link-square\"></i>\n" +
    "          </span>\n" +
    "          <input type=\"text\" class=\"form-control\" readonly\n" +
    "            value=\"<style>.babbage-embed{position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;} .babbage-embed iframe{position:absolute;top:0;left:0;width:100%;height:100%;}</style><div class='babbage-embed'><iframe src='{{embedLink}}' frameborder='0' allowfullscreen></iframe></div>\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "\n" +
    "    </div>\n" +
    "  </div>\n" +
    "</babbage>\n" +
    "");
}]);
