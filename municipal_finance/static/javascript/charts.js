var Chart = function() {
  var self = this;

  self.init = function() {
    self.format = d3_format
        .formatLocale({decimal: ".", thousands: " ", grouping: [3], currency: "R"})
        .format(",.0f");

    self.drawChart(CASH_COVERAGE, 'cash-coverage');
    self.drawChart(CASH_AT_YEAR_END, 'cash-at-year-end');
    self.drawChart(OP_BUDGET_DIFF, 'op-budget-diff');
    self.drawChart(CAP_BUDGET_DIFF, 'cap-budget-diff');
    self.drawChart(REP_MAINT_PERC_PPE, 'rep-maint-perc-ppe');
  };

  self.getContainerObject = function(container) {
    self.container = $("." + container + ".chart-container");
  }

  self.setDimensions = function (container) {
    var container_width = self.container.width();
    var container_height = self.container.closest('.indicator').height();

    self.margin = {top: 20, right: 20, bottom: 30, left: 20};
    self.width = container_width - self.margin.left - self.margin.right;
    self.height = container_height - self.margin.top - self.margin.bottom;

    self.x = d3.scale.ordinal()
        .rangeRoundBands([0, self.width], 0.85);

    self.y = d3.scale.linear()
        .range([self.height, 0]);

    self.xAxis = d3.svg.axis()
        .scale(self.x)
        .orient("bottom")
        .tickSize(0, 0)
        .tickPadding(10);
  };

  self.drawChart = function(data, container) {
    self.getContainerObject(container);
    self.container.empty();
    self.setDimensions(container);

    self.svg = d3.select("." + container + ".chart-container").append("svg")
        .attr("width", self.width + self.margin.left + self.margin.right)
        .attr("height", self.height + self.margin.top + self.margin.bottom)
      .append("g")
        .attr("transform", "translate(" + self.margin.left + "," + self.margin.top + ")");

    self.x.domain(data.map(function(d) { return d.year; }));
    self.y.domain([0, d3.max(data, function(d) { return d.result; })]);

    //  Draw the x-axis
    self.svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + self.height + ")")
      .call(self.xAxis);

    //  Draw the bars
    self.svg.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "chart-bar")
        .attr("x", function(d) { return self.x(d.year); })
        .attr("width", self.x.rangeBand())
        .attr("y", function(d) { return self.y(d.result); })
        .attr("height", function(d) { return self.height - self.y(d.result); })
        .attr("class", function(d, i){
          if (i === 0) {
            return "current " + d.rating;
          } else {
            return "historical " + d.rating;
          }
        });

    // Add the labels
    self.svg.selectAll("text.bar")
        .data(data)
      .enter().append("text")
        .attr("class", "bar-label")
        .attr("text-anchor", "middle")
        .attr("x", function(d) { return self.x(d.year) + self.x.rangeBand()/2; })
        .attr("y", function(d) { return self.y(d.result) - 5; })
        .attr("class", function(d, i){
          if (i === 0) {
            return "current";
          } else {
            return "historical";
          }
        })
        .text(function(d) {
          if (d.result >= 1000) {
            var format = d3.formatPrefix(1000);
            return self.format(format.scale(d.result)) + " " + format.symbol;
          } else {
            return d.result;
          }

         });
  };
};

var chart = new Chart();
chart.init();

$(window).on('resize', function(){
  _.debounce(chart.init(), 300);
});
