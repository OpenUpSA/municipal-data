var getNumberFormat = function() {
  return d3_format
        .formatLocale({decimal: ".", thousands: " ", grouping: [3], currency: "R"})
        .format(",.0f");
};

function wrapText(text, width) {
  // see https://bl.ocks.org/mbostock/7555321
  text.each(function() {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        x = text.attr("x"),
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("y", y).attr("dy", dy + "em");

    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}

var HorizontalGroupedBarChart = function() {
  var self = this;

  self.init = function() {
    self.format = getNumberFormat();

    $('.chart-container[data-chart^=grouped-bar-]').each(function() {
      var $container = $(this),
          name = $container.data('chart').substring(12),
          data = profileData.indicators;

      // find nested data
      _.each(name.split("."), function(p) { data = data[p]; });

      self.drawChart(data, name, $container);
    });
  };

  self.setDimensions = function() {
    var container_width = self.container.width();
    var container_height = 300;

    if (self.container.hasClass('tall')) container_height = container_height * 2;

    self.margin = {top: 10, right: 0, bottom: 10, left: 200};
    self.width = container_width - self.margin.left - self.margin.right;
    self.height = container_height - self.margin.top - self.margin.bottom;

    self.y0 = d3.scale.ordinal()
        .rangeRoundBands([0, self.height], 0.2);

    self.y1 = d3.scale.ordinal();

    self.x = d3.scale.linear()
        .range([0, self.width]);

    self.yAxis = d3.svg.axis()
        .scale(self.y0)
        .orient("left")
        .tickSize(0, 0)
        .tickPadding(10);
  };

  self.color = d3.scale.ordinal()
    .range(["#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]);

  self.drawChart = function(data, name, $container) {
    self.container = $container.empty();
    self.setDimensions();

    self.svg = d3.select($container[0]).append("svg")
        .attr("width", self.width + self.margin.left + self.margin.right)
        .attr("height", self.height + self.margin.top + self.margin.bottom)
      .append("g")
        .attr("transform", "translate(" + self.margin.left + "," + self.margin.top + ")")
        .attr("class", "grouped-bar");

    var years = _.keys(_.countBy(data, function(data) { return data.year; })).reverse();
    var items = _.keys(_.countBy(data, function(data) { return data.item; }));

    var groupedData = [];

    items.forEach(function(item){
      var val =[];
      data.forEach(function (d) {
        if(item == d.item){
          val.push(d);
        }
      });
      groupedData.push({item: item, values: val});
    });

    self.y0.domain(groupedData.map(function(d) { return d.item; }));
    self.y1.domain(years).rangeRoundBands([0, self.y0.rangeBand()]);

    self.x.domain([0, d3.max(data, function(d) { return d.amount; })]);

    //  Draw the y-axis
    self.svg.append("g")
      .attr("class", "y axis")
      .call(self.yAxis)
      .selectAll(".tick text")
        .call(wrapText, self.margin.left - 10);

    // Create the groups
    var group = self.svg.selectAll(".group")
        .data(groupedData)
      .enter().append("g")
        .attr("class", "group")
        .attr("transform", function(d) { return "translate(0," + self.y0(d.item) + ")"; });

    //  Draw the bars
    group.selectAll(".chart-bar")
        .data(function(d) { return d.values; })
      .enter().append("rect")
        .attr("class", "chart-bar")
        .attr("y", function(d) { return self.y1(d.year); })
        .attr("height", self.y1.rangeBand() - 1)
        .attr("width", function(d) { return self.x(d.amount); })
        .style("fill", function (d) { return self.color(d.year); });

    var legend = self.svg.selectAll(".legend")
        .data(years)
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + (self.height - (years.length - i + 1) * 20) + ")"; });

    legend.append("rect")
        .attr("x", self.width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", function (d) { return self.color(d); });

    legend.append("text")
        .attr("x", self.width - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });

  };
};


var VerticalBarChart = function() {
  var self = this;

  self.init = function() {
    self.format = getNumberFormat();

    $('.chart-container[data-chart^=column-]').each(function() {
      var $container = $(this),
          name = $container.data('chart').substring(7),
          data = profileData.indicators;

      // find nested data
      _.each(name.split("."), function(p) { data = data[p]; });

      self.drawChart(data, name, $container);
    });
  };

  self.setDimensions = function() {
    var container_width = self.container.width();
    var container_height = 150;

    self.margin = {top: 20, right: 0, bottom: 20, left: 0};
    self.width = container_width - self.margin.left - self.margin.right;
    self.height = container_height - self.margin.top - self.margin.bottom;

    self.x = d3.scale.ordinal()
        .rangeRoundBands([0, self.width], 0.5);

    self.y = d3.scale.linear()
        .range([self.height, 0]);

    self.xAxis = d3.svg.axis()
        .scale(self.x)
        .orient("bottom")
        .tickSize(0, 0)
        .tickPadding(10);
  };

  self.drawChart = function(data, name, $container) {
    self.container = $container.empty();
    self.setDimensions();

    self.svg = d3.select($container[0]).append("svg")
        .attr("width", self.width + self.margin.left + self.margin.right)
        .attr("height", self.height + self.margin.top + self.margin.bottom)
      .append("g")
        .attr("transform", "translate(" + self.margin.left + "," + self.margin.top + ")");

    self.x.domain(data.map(function(d) { return d.year; }));
    self.y.domain([
      Math.min(d3.min(data, function(d) { return d.result; }), 0),
      Math.max(d3.max(data, function(d) { return d.result; }), 0)
    ]);

    //  Draw the x-axis
    self.svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + self.height + ")")
      .call(self.xAxis);

    // Draw the zero line
    self.svg.append("g")
        .attr("class", "x axis zero")
        .attr("transform", "translate(0," + self.y(0) + ")")
        .call(self.xAxis.tickFormat("").tickSize(0));

    //  Draw the bars
    self.svg.selectAll(".chart-bar")
        .data(data)
      .enter().append("rect")
        .attr("x", function(d) { return self.x(d.year); })
        .attr("width", self.x.rangeBand())
        .attr("y", function(d) { return self.y(Math.max(d.result, 0)); })
        .attr("height", function(d) { return Math.abs(self.y(d.result) - self.y(0)); })
        .attr("class", function(d) {
          return "chart-bar " + d.rating;
        });

    // Add the labels
    self.svg.selectAll("text.bar")
        .data(data)
      .enter().append("text")
        .attr("class", "bar-label")
        .attr("text-anchor", "middle")
        .attr("x", function(d) { return self.x(d.year) + self.x.rangeBand()/2; })
        .attr("y", function(d) { return self.y(Math.max(d.result, 0)) - 5; })
        .text(function(d) {
          if (Math.abs(d.result) >= 1000) {
            var format = d3.formatPrefix(1000);
            return self.format(format.scale(d.result)) + " " + format.symbol;
          } else {
            return d.result;
          }

         });
  };
};

var vertical_bar_chart = new VerticalBarChart();
var horizontal_bar_chart = new HorizontalGroupedBarChart();

vertical_bar_chart.init();
horizontal_bar_chart.init();

$(window).on('resize', function(){
  _.debounce(vertical_bar_chart.init(), 300);
  _.debounce(horizontal_bar_chart.init(), 300);
});
