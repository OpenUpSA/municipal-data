var formatLocale = d3_format.formatLocale({decimal: ".", thousands: " ", grouping: [3], currency: ["R", ""]});

var formats = {
  currency: formatLocale.format("$,.0f"),
  percent: function(n) {
    if (n === null)
      return "";
    else
      return formatLocale.format(",.1f")(n) + "%";
  },
  num: function(n, name) {
    if (n === null)
      return "";
    else
      return formatLocale.format(",.1f")(n) + (name ? " " + name : "");
  },
  terse: function(n, f) {
    var format;

    if (n === null) {
      return "";
    } else {
      if (Math.abs(n) >= 1000 * 1000 * 1000) {
        format = d3.formatPrefix(1000 * 1000);
        return f(format.scale(n)) + format.symbol;
      } else if (Math.abs(n) >= 1000) {
        format = d3.formatPrefix(1000);
        return f(format.scale(n)) + format.symbol;
      } else {
        return f(n);
      }
    }
  },
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

var tooltip = d3.select("body").append("div")
  .attr("class", "chart-tooltip")
  .style("opacity", 0);

function showTooltip(html) {
  tooltip
    .style("opacity", 1)
    .html(html);
  moveTooltip();
}

function moveTooltip() {
  var height = tooltip.node().getBoundingClientRect().height;
  tooltip
    .style("left", (d3.event.pageX) + "px")
    .style("top", (d3.event.pageY - 20 - height) + "px");
}

function hideTooltip() {
  tooltip.style("opacity", 0);
}

var HorizontalGroupedBarChart = function() {
  var self = this;

  self.discover = function() {
    // find all charts
    $('.chart-container[data-chart^=grouped-bar-]').each(function() {
      var chart = new HorizontalGroupedBarChart();
      chart.init(this);
      $(window).on('resize', _.debounce(chart.drawChart, 300));
    });
  };

  self.init = function(container) {
    self.container = $(container);
    self.name = self.container.data('chart').substring(12);

    // find nested data
    var data = profileData.indicators;
    _.each(self.name.split("."), function(p) { data = data[p]; });

    self.data = data.values;
    self.drawChart();
  };

  self.setDimensions = function(items) {
    var container_width = self.container.width();
    var container_height = (items > 5 ? 10 : 13) * items;
    var narrow = document.documentElement.clientWidth < 768;

    if ($('body').hasClass('print')) container_width = 550;

    self.margin = {top: 10, right: 0, bottom: 10, left: narrow ? 120 : 200};
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

  self.drawChart = function() {
    var data = self.data,
        name = self.name,
        dates = _.keys(_.countBy(data, function(data) { return data.date; })).reverse(),
        items = _.keys(_.countBy(data, function(data) { return data.item; }));

    self.container.empty();
    self.setDimensions(dates.length * items.length);

    self.svg = d3.select(self.container[0]).append("svg")
        .attr("width", self.width + self.margin.left + self.margin.right)
        .attr("height", self.height + self.margin.top + self.margin.bottom)
      .append("g")
        .attr("transform", "translate(" + self.margin.left + "," + self.margin.top + ")")
        .attr("class", "grouped-bar");

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
    self.y1.domain(dates).rangeRoundBands([0, self.y0.rangeBand()]);

    self.x.domain([0, d3.max(data, function(d) { return d.percent; })]);

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
        .attr("y", function(d) { return self.y1(d.date); })
        .attr("height", self.y1.rangeBand() - 1)
        .attr("width", function(d) { return self.x(d.percent); })
        .style("fill", function (d) { return self.color(d.date); })
        .on("mouseover", function(d) {
          showTooltip(self.formatTooltip(d));
        })
        .on("mousemove", moveTooltip)
        .on("mouseout", hideTooltip);

    var legend = self.svg.selectAll(".legend")
        .data(dates)
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + (self.height - (dates.length - i + 1) * 20) + ")"; });

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

  self.formatTooltip = function(d) {
    return "<b>" + d.date + ":</b> " + formats.percent(d.percent) + "<br>" + formats.currency(d.amount);
  };
};


var VerticalBarChart = function() {
  var self = this;

  self.discover = function() {
    // find all charts
    $('.chart-container[data-chart^=column-]').each(function() {
      var chart = new VerticalBarChart();
      chart.init(this);
      $(window).on('resize', _.debounce(chart.drawChart, 300));
    });
  };

  self.init = function(container) {
    self.container = $(container);
    self.name = self.container.data('chart').substring(7);

    // find nested data
    var data = profileData.indicators;
    _.each(self.name.split("."), function(p) { data = data[p]; });

    self.data = data;
    // earliest to latest
    self.data.values.reverse();

    // establish format
    self.format = formats[self.container.data('unit') || "currency"];
    self.unit_name = self.container.data('unit-name');
    self.drawChart();
  };

  self.setDimensions = function() {
    var container_width = self.container.width();
    var container_height = 150;

    if ($('body').hasClass('print')) container_width = 300;

    self.margin = {top: 20, right: 0, bottom: 25, left: 0};
    self.width = container_width - self.margin.left - self.margin.right;
    self.height = container_height - self.margin.top - self.margin.bottom;

    self.x = d3.scale.ordinal()
        .rangeRoundBands([0, self.width], 0.3, 0.1);

    self.y = d3.scale.linear()
        .range([self.height, 0]);

    self.xAxis = d3.svg.axis()
        .scale(self.x)
        .orient("bottom")
        .tickSize(0, 0)
        .tickPadding(10);
  };

  self.drawChart = function() {
    var data = self.data.values,
        comparisons = self.data.comparisons;

    self.container.empty();
    self.setDimensions();

    self.svg = d3.select(self.container[0]).append("svg")
        .attr("width", self.width + self.margin.left + self.margin.right)
        .attr("height", self.height + self.margin.top + self.margin.bottom)
      .append("g")
        .attr("transform", "translate(" + self.margin.left + "," + self.margin.top + ")");

    self.x.domain(data.map(function(d) { return d.date; }));
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

    //  Draw the columns
    self.svg.selectAll(".chart-column")
        .data(data)
      .enter().append("rect")
        .attr("x", function(d) { return self.x(d.date); })
        .attr("width", self.x.rangeBand())
        .attr("y", function(d) { return self.y(Math.max(d.result, 0)); })
        .attr("height", function(d) { return Math.abs(self.y(d.result) - self.y(0)); })
        .attr("class", function(d) {
          return "chart-column " + d.rating;
        })
        .on("mouseover", function(d) {
          showTooltip(self.formatTooltip(d, comparisons && comparisons[d.date]));
        })
        .on("mousemove", moveTooltip)
        .on("mouseout", hideTooltip);

    // Add the labels
    self.svg.selectAll("text.bar")
        .data(data)
      .enter().append("text")
        .attr("class", "column-label")
        .attr("text-anchor", "middle")
        .attr("x", function(d) { return self.x(d.date) + self.x.rangeBand()/2; })
        .attr("y", function(d) { return self.y(Math.max(d.result, 0)) - 5; })
        .text(function(d) { return formats.terse(d.result, self.format); });
  };

  self.formatTooltip = function(d, comparisons) {
    var t = "<b>" + d.date + ":</b> " + self.format(d.result, self.unit_name);

    if (comparisons && comparisons.length > 0) {
      t += '<ul class="comparatives">';
      t += _.map(comparisons, function(cmp) {
        return '<li>' + cmp.comparison + ' similar municipalities ' + cmp.place + ': ' + self.format(cmp.value, self.unit_name) + '</li>';
      }).join(' ');
    }

    return t;
  };
};

var SimpleBarChart = function() {
    var self = this;

    self.discover = function() {
        $('.simple-barchart').each(function() {
             var chart = new SimpleBarChart();
             chart.init(this);
             $(window).on('resize', _.debounce(chart.drawChart, 300));
        });
    };

    self.init = function(container) {
        self.container = $(container);
        indicator = self.container.data("indicator");
        self.data = profileData.indicators[indicator];
        self.drawChart();
    };

    self.drawChart = function() {

        var chart = c3.generate({
            bindto: self.container[0],
            data: {
                json: self.data,
                keys: {
                    x : "label",
                    value : ["value"]
                },
                type: "bar",
            },
            axis: {
                x : { type : "category" }
            },
            bar: {
                width: {
                    ratio: 0.8
                }
            }
        })
    }
}

var SimpleLineChart = function() {
    var self = this;

    self.discover = function() {
        $('.simple-linechart').each(function() {
             var chart = new SimpleLineChart();
             chart.init(this);
             $(window).on('resize', _.debounce(chart.drawChart, 300));
        });
    };

    self.init = function(container) {
        self.container = $(container);
        indicator = self.container.data("indicator");
        self.data = profileData.indicators[indicator];
        self.drawChart();
    };

    self.drawChart = function() {

        var chart = c3.generate({
            bindto: self.container[0],
            data: {
                json: self.data,
                keys: {
                    x : "label",
                    value : ["value"]
                },
                type: "line",
            },
        })
    }
}

var IncomeSplitPieChart = function() {
  var self = this;

  self.discover = function() {
    // find all charts
    $('#income-split-pie').each(function() {
      var chart = new IncomeSplitPieChart();
      chart.init(this);
      $(window).on('resize', _.debounce(chart.drawChart, 300));
    });
  };

  self.init = function(container) {
    self.container = $(container);
    self.color = d3.scale.ordinal()
      .range(["#bcbd22", "#17becf"]);
    self.data = [{
        name: "From Government",
        amount: profileData.indicators.revenue_sources.government.amount,
      }, {
        name: "Generated locally",
        amount: profileData.indicators.revenue_sources.local.amount,
      }];

    self.drawChart();
  };

  self.drawChart = function() {
    self.container.empty();
    self.setDimensions();

    self.svg = d3.select(self.container[0]).append("svg")
        .attr("width", self.width)
        .attr("height", self.height)
      .append("g")
        .attr("transform", "translate(" + self.width / 2 + "," + self.height / 2 + ")")
        .attr("class", "pie");

    var arc = d3.svg.arc()
        .outerRadius(self.radius - 10)
        .innerRadius(0);

    var pie = d3.layout.pie()
        .sort(null)
        .value(function(d) { return d.amount; });

    var g = self.svg.selectAll(".arc")
        .data(pie(self.data))
      .enter().append("g")
        .attr("class", "arc");

    g.append("path")
        .attr("d", arc)
        .style("fill", function(d) { return self.color(d.data.name); });
  };

  self.setDimensions = function() {
    self.width = self.container.width();
    if ($('body').hasClass('print')) self.width = 100;

    self.width = Math.min(self.width, 150);
    self.height = self.width;
    self.radius = Math.min(self.width, self.height) / 2;

  };
};

$(function() {
  new VerticalBarChart().discover();
  new HorizontalGroupedBarChart().discover();
  new IncomeSplitPieChart().discover();
  new SimpleBarChart().discover();
  new SimpleLineChart().discover();

});
