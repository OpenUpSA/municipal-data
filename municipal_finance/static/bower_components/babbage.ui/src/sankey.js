
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
      var dfd = $http.get(babbageCtrl.getApiUrl('aggregate'),
                          babbageCtrl.queryParams(q));

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
