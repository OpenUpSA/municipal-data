import { format as d3Format } from 'd3-format';
import { axisLeft, axisBottom } from 'd3-axis';
import { scaleBand, scaleLinear } from 'd3-scale';
import { max as d3Max } from 'd3-array';
import { select as d3Select } from 'd3-selection';
import { transition } from 'd3-transition';

const TICKS = 5;

const formatRand = (x, decimals, randSpace) => {
  decimals = decimals === undefined ? 1 : decimals;
  randSpace = randSpace === undefined ? ' ' : '';
  return `R${randSpace}${d3Format(`,.${decimals}f`)(x)}`;
};

const humaniseRand = (x, longForm) => {
  longForm = longForm === undefined ? true : longForm;
  const randSpace = longForm ? ' ' : '';
  const decimals = longForm ? 1 : 0;
  const suffixBillion = longForm === true ? ' billion' : 'bn';
  const suffixMillion = longForm === true ? ' million' : 'm';
  const suffixThousand = longForm === true ? '  thousand' : 'k';

  if (Math.abs(x) >= 1000000000) {
    return formatRand(x / 1000000000, decimals, randSpace) + suffixBillion;
  } if (Math.abs(x) >= 1000000) {
    return formatRand(x / 1000000, decimals, randSpace) + suffixMillion;
  } if (!longForm && Math.abs(x) >= 100000) {
    return formatRand(x / 1000, decimals, randSpace) + suffixThousand;
  }
  return formatRand(x, 0);
};

const formatter = (d, resultType) => {
  if(resultType == 'currency') {
    return humaniseRand(d, false);
  }
  else if(resultType == 'months') {
    return Math.round(d * 10) / 10;
  }
  else if(resultType == 'percentage') {
    return Math.round(d * 10) / 10 + '%';
  }
  else if(resultType == 'ratio') {
    return Math.round(d * 10) / 10;
  }
  else {
    return d;
  }
};

export class ColumnChart {
  constructor(container, muniData) {
    this.svg = undefined;
    this.margin = {top: 50, right: 20, bottom: 50, left: 50};
    this.x = {};
    this.y = {};
    this.height = undefined;
    this.width = undefined;
    this.xAxis = undefined;
    this.yAxis = undefined;

    this._drawMuniChart(container, muniData);
  }

  x_gridlines() {
    return axisLeft(this.y).ticks(TICKS);
  }

  _drawMuniChart(container, muniData) {

    this.width = document.querySelector(container).offsetWidth - this.margin.left - this.margin.right,
    this.height = 300 - this.margin.top - this.margin.bottom;

    this.x = scaleBand().range([0, this.width]).paddingInner(0.2);
    this.y = scaleLinear().range([this.height, 0]);

    this.xAxis = axisBottom()
      .scale(this.x);

    this.yAxis = axisLeft()
      .scale(this.y)
      .ticks(TICKS)
      .tickFormat(function(d) {
        return formatter(d, muniData[0].resultType);
      });

    this.svg = d3Select(container).append("svg")
      .attr("width", this.width + this.margin.left + this.margin.right)
      .attr("height", this.height + this.margin.top + this.margin.bottom)
      .append("g")
      .attr('class','muniChart')
      .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

    this._setAxes(muniData);

    this.svg.append('g').attr('class', 'chartData');

    this.svg.append('g').attr('class', 'medians');

    this._addMedians(muniData);

    this.loadData(muniData);
  }

  _setAxes(muniData) {

    this.x.domain(muniData[0].data.map(function(d) { return d.period; }));

    this.muniMaxes = muniData.map(function(d) { return d3Max(d.data, function(e) { return e.value; }); } );

    this.y.domain([0, d3Max(this.muniMaxes, function(d) { return d; })]);

    this.svg.append("g")
      .datum(muniData[0].data.map(function(d) { return d.period; }))
      .attr("class", "x axis")
      .attr("transform", "translate(0," + this.height + ")")
      .call(this.xAxis);

    this.svg.append("g")
      .attr("class", "y axis")
      .call(this.yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 10);

    this.svg.append("g")
      .attr("class", "grid")
      .call(this.x_gridlines()
            .tickSize(- this.width)
            .tickFormat("")
           );
  }

  _adjustY(max) {

    this.y.domain([0, max]);

    this.svg.select('.y')
      .transition().duration(1500)
      .call(this.yAxis);

    this.svg.select('.grid')
      .transition().duration(1500)
      .call(this.x_gridlines()
            .tickSize(- this.width)
            .tickFormat("")
           );

  }

  adjustBars(muniCount) {

    this.svg.selectAll('.bar')
      .transition().delay(function(i) { return i * 50; }).duration(1000)
      .attr('height', function(d) { return this.height - this.y(d); })
      .attr('width', this.x.bandwidth() / muniCount)
      .attr("y", function(d) { return this.y(d) });

    // svg.selectAll('.label')
    //     .transition().delay(function(i) { return i * 200 }).duration(1500)
    //     .attr("y", function(d) { return y(d) - 40 })

    // svg.selectAll('.label rect')
    //     .transition().delay(function(i) { return i * 200 }).duration(1500)
    //     .attr("y", function(d) { return y(d) - 40 -5 })

    // svg.selectAll('.label text')
    //     .transition().delay(function(i) { return i * 200 }).duration(1500)
    //     .attr("y", function(d) { return y(d) - 40 })

  }

  _addMedians(muniData) {
    const categoryCount = muniData[0].data.map(function(d) { return d.period; });

    for(let i = 0; i < categoryCount.length; i++) {

      this.svg.select('g.medians')
        .append('line')
        .attr('period',categoryCount[i])
        .attr('value',0)
        .attr('class','median')
        .attr('stroke','#000')
        .attr("x1", this.x(categoryCount[i]) )
        .attr("x2", this.x(categoryCount[i]) + this.x.bandwidth())
        .attr("y1", this.y(0))
        .attr("y2", this.y(0))
        .attr("height", 1)
        .attr('stroke-dasharray','5px')
        .attr('opacity',0);
    }
  }

  loadMedians(medians) {
    medians.forEach((function(median, i) {
      this.svg.select('line.median[period="' + median.period + '"]')
        .transition().delay( i * 200 ).duration(500)
        .attr('y1', this.y(median.value))
        .attr('y2', this.y(median.value))
        .attr('opacity',1)
        .attr('value', median.value);
    }).bind(this));


  }

  adjustMedians() {
    let medians = this.svg.selectAll('line.median');
    medians._groups[0].forEach(function(median, index) {
      this.svg.select('line.median[period="' + median.attributes['period'].value +'"]')
        .transition().duration(500)
        .attr('y1', this.y(median.attributes['value'].value))
        .attr('y2', this.y(median.attributes['value'].value));
    });
  }

  removeMedians() {
    let medians = this.svg.selectAll('line.median');
    medians._groups[0].forEach((function(median, index) {
      this.svg.select('line.median[period="' + median.attributes['period'].value +'"]')
        .transition().duration(500)
        .attr('y1', this.y(0))
        .attr('y2', this.y(0))
        .attr('opacity', 0);
    }).bind(this));
  }

  loadData(muniData) {
    let activeMunis = 0;
    if (this.svg.selectAll('g.chartData > g')._groups[0].length > 0) {

      activeMunis = this.svg.selectAll('g.chartData > g')._groups[0].length;
      let muniMax = d3Max(muniData.map(function(d) {
        return d3Max(d.data, function(e) { return e.value; });
      }));
      this.adjustY(muniMax);
      this.adjustBars(activeMunis + muniData.length);
      this.adjustMedians();
    }


    // Resize activeMunis

    // svg.selectAll('.bar')
    //     .transition().delay(function(i) { return i * 200 }).duration(500)
    //     .attr('width', x.bandwidth() / (muniData.length + activeMunis))

    // svg.selectAll('.label')
    //     .transition().delay(function(i) { return i * 200 }).duration(1500)
    //     .attr("x", function(d) { return y(d) - 40 })

    // svg.selectAll('.label rect')
    //     .transition().delay(function(i) { return i * 200 }).duration(1500)
    //     .attr("x", x.bandwidth() / (muniData.length + activeMunis) )

    // svg.selectAll('.label text')
    //     .transition().delay(function(i) { return i * 200 }).duration(1500)
    //     .attr("x", function(d) { return y(d) - 40 })


    muniData.forEach((function(muni ,muniIndex) {

      this.svg.selectAll('.chartData')
        .append('g')
        .attr('id', 'data-' + muni.municipality.code)
        .attr('muni', muni.municipality.code);

      muni.data.forEach((function(data, dataIndex) {

        this.svg.selectAll('#data-' + muni.municipality.code)
          .append('g')
          .attr('class', 'barGroup')
          .attr('muni', muni.municipality.code)
          .attr('period', data.period)
          .attr('value', data.value)
          .attr('index', dataIndex);

        this.svg.select('#data-' + muni.municipality.code + ' g[index="' + dataIndex + '"]')
          .append('rect')
          .datum(data.value)
          .attr('class','bar')
          .attr('fill',data.fillColor)
          .attr("x", this.x(data.period) + ((muniIndex + activeMunis) * this.x.bandwidth() / (muniData.length + activeMunis)) + (dataIndex + 1 * 5) )
          .attr("width", (this.x.bandwidth()) / (muniData.length + activeMunis) - 5)
          .attr("y", this.y(0))
          .attr("height", 0 )
          .transition().delay( dataIndex * 200 ).duration(500)
          .attr("y", this.y(data.value))
          .attr("height", this.height - this.y(data.value));

        // let relatedRect = svg.select('#data-' + muni.municipality.code + ' g[index="' + dataIndex + '"] rect.bar')
        // let labelX = parseInt(relatedRect.attr('x')) + parseInt(relatedRect.attr('width')/2)
        // let labelY = y(data.value) - 40

        // svg.select('#data-' + muni.municipality.code + ' g[index="' + dataIndex + '"]')
        //     .append('g')
        //         .datum(data.value)
        //         .attr('class','label')
        //         .attr('x', labelX)
        //         .attr('y', labelY)
        //         .attr('opacity', 0)

        // svg.select('#data-' + muni.municipality.code + ' g[index="' + dataIndex + '"] g.label')
        //     .append('rect')
        //         .attr('x', labelX - 5)
        //         .attr('y', labelY - 4)
        //         .attr('ry', 5)
        //         .attr('rx', 5)
        //         .attr('fill','#ccc')
        //         .attr('width', 0)
        //         .attr('height', 0)


        // svg.select('#data-' + muni.municipality.code + ' g[index="' + dataIndex + '"] g.label')
        //     .append('text')
        //         .attr("dy", ".75em")
        //         .attr('x',labelX)
        //         .attr('y', labelY)
        //         .text(data.value)

        // svg.select('#data-' + muni.municipality.code + ' g[index="' + dataIndex + '"] g.label rect')
        //     .attr('width', svg.select('#data-' + muni.municipality.code + ' g[index="' + dataIndex + '"] g.label text').attr('width') + 20)
        //     .attr('height', svg.select('#data-' + muni.municipality.code + ' g[index="' + dataIndex + '"] g.label text').attr('height') + 20)

        // svg.select('#data-' + muni.municipality.code + ' g[index="' + dataIndex + '"] g')
        //     .transition().delay(dataIndex * 100).duration(500)
        //     .attr('opacity',1)

      }).bind(this));
    }).bind(this));

    return;
  }

  removeData(ids) {
    let max = this.y.domain()[1];

    ids.forEach(function(muni, i) {
      this.svg.selectAll('#data-' + muni + ' .label')
        .transition().duration(500)
        .attr("opacity", 0)
        .remove();

      this.svg.selectAll('#data-' + muni + ' .bar')
        .transition().duration(500)
        .attr("y", this.y(0))
        .attr("height", 0 );

      this.svg.select('#data-' + muni)
        .remove();
    });

    let currentMaxes = [];

    let currentMunis = this.svg.selectAll('g.barGroup[muni]');
    currentMunis._groups[0].forEach(function(muni) {
      currentMaxes.push(muni.attributes['value'].value);
    });

    this.adjustY(d3Max(currentMaxes));
    this.adjustBars(this.svg.selectAll('g.chartData > g')._groups[0].length);
    this.adjustMedians();
  }
};
