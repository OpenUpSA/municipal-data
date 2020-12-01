import { format as d3Format } from 'd3-format';
import { axisLeft, axisBottom } from 'd3-axis';
import { scaleBand, scaleLinear } from 'd3-scale';
import { max as d3Max, thresholdSturges } from 'd3-array';
import { min as d3Min } from 'd3-array';
import { select as d3Select, selectAll } from 'd3-selection';
import { transition } from 'd3-transition';

const HEIGHT = 300;
const TICKS = 5;

const formatRand = (x, decimals, randSpace) => {
  decimals = decimals === undefined ? 1 : decimals;
  randSpace = randSpace === undefined ? ' ' : '';
  return `R${randSpace}${d3Format(`,.${decimals}f`)(x)}`;
}

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
}

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
}

export default class ColumnChart {
  constructor(container, muniData) {
     this.chart = {
        config: {
            bindto: container,
            margin: { top: 50, right: 10, bottom: 20, left: 50 },
            x: {},
            y: {},
            height: 0,
            width: 0,
            xAxis: 0,
            yAxis: 0
        },
        c: {},
        data: muniData,
        medians: []
    }

    this._drawColumnChart();
  }

  x_gridlines() {
    return axisLeft(this.chart.config.y).ticks(TICKS);
  }

  _drawColumnChart(container, muniData) {

    this.chart.config.width = document.querySelector(this.chart.config.bindto).offsetWidth - this.chart.config.margin.left - this.chart.config.margin.right,
    this.chart.config.height = HEIGHT - this.chart.config.margin.top - this.chart.config.margin.bottom;

    this.chart.config.x = scaleBand().range([0, this.chart.config.width]).paddingInner(0.2)
    this.chart.config.y = scaleLinear().range([this.chart.config.height, 0])

    this.chart.config.xAxis = axisBottom()
        .scale(this.chart.config.x)

    this.chart.config.yAxis = axisLeft()
        .scale(this.chart.config.y)
        .ticks(TICKS)
        .tickFormat((d) => {
            return formatter(d, this.chart.data[0].resultType)
        })

    this._loadFilters()

    this.chart.c = d3Select(this.chart.config.bindto).append("svg")
        .attr("width", this.chart.config.width + this.chart.config.margin.left + this.chart.config.margin.right)
        .attr("height", this.chart.config.height + this.chart.config.margin.top + this.chart.config.margin.bottom)
        .append("g")
        .attr('class','muniChart')
        .attr("transform", "translate(" + this.chart.config.margin.left + "," + this.chart.config.margin.top + ")")

    this._setAxes()

    this.chart.c.append('g')
      .attr('class', 'chartData')
      .attr('width', this.chart.config.width)
      .attr('x', 0)
      .attr('y', 0)
      .attr('height', this.chart.config.height)

    this.chart.c.append('g')
      .attr('class', 'medians')


    this.loadData(this.chart.data)


  }

  _setAxes() {

    let periodArray = this.chart.data[0].data.map(function(d) { return d.period } )

    this.chart.config.x.domain(periodArray)

    let muniMaxes = this.chart.data.map(function(d) { return d3Max(d.data, function(e) { return e.value }) } )

    this.chart.config.y.domain([0, d3Max(muniMaxes, function(d) { return d })])


    this.chart.c.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + this.chart.config.height + ")")
        .call(this.chart.config.xAxis)

    this.chart.c.append("g")
        .attr("class", "y axis")
        .call(this.chart.config.yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 10)

    this.chart.c.append("g")
        .attr("class", "grid")
        .call(this.x_gridlines()
        .tickSize(-this.chart.config.width)
        .tickFormat("")
        )

    let medianArray = []

    periodArray.forEach(p => medianArray.push({period: p, value: 0}))

    this.chart.medians = medianArray

    this.loadMedians(this.chart.medians, true)

  }



  _adjustY() {


    let dataMax = d3Max(this.chart.data.map(d => d3Max(d.data.map(e => e.value))))
    let dataMin = d3Min(this.chart.data.map(d => d3Min(d.data.map(e => e.value))))

    let medianMax = d3Max(this.chart.medians.map(d => d.value))
    let medianMin = d3Min(this.chart.medians.map(d => d.value))

    let max = d3Max([dataMax, medianMax])
    let min = d3Min([dataMin, medianMin])

    min = min > 0 ? 0 : min
    max = max < 0 ? 0 : max

    this.chart.config.y.domain([min, max]);

    this.chart.c.select('.y')
      	.transition().duration(500)
      	.call(this.chart.config.yAxis);

    this.chart.c.select('.grid')
      	.transition().duration(500)
      	.call(this.x_gridlines()
        	.tickSize(- this.chart.config.width)
            .tickFormat("")
        )

  }

	loadData(incomingData, adjustMedians = true) {

    let self = this;

    self.chart.data = incomingData

	  self._adjustY()

    let newData = []

    self.chart.data.forEach(function(d) {
      	d.data.forEach(function(muniData) {
        	newData.push({
          		municipality: d.municipality,
          		value: muniData.value,
          		fillColor: muniData.fillColor,
          		period: muniData.period
        	})
      	})
    })


    let chartData = d3Select(this.chart.config.bindto + ' .chartData')

	  let colGroups = chartData.selectAll('.colGroup')
    	.data(newData);

    colGroups.exit().remove()

    let col = colGroups.enter().append('g')
        .attr('class','colGroup')
        .attr('colid', d => d.municipality.code)
        .attr('value',d =>  d.value)
        .on('mouseover',self._colMouseOver.bind(self))
        .on('mouseout',self._colMouseOut.bind(self))

    // col.append('path')
    //     .attr('class','rect')

    col.append('rect')
        .attr('class','rect')

    col.append('rect')
        .attr('class','labelBackground')

    col.append('text')
        .attr('class','label')

    colGroups = colGroups.merge(col)

    colGroups.select('.rect')
      .attr('fill', d => d.fillColor)
      // .attr('y', self.chart.config.y(0))
      .attr('x', function(d,i,a) {
          let periodArray =  newData.filter( obj => obj.period === d.period ).map( obj => obj.municipality.code );
          let elementIndex = periodArray.findIndex( o => o == d.municipality.code)
          return self.chart.config.x(d.period) + (self.chart.config.x.bandwidth() / 8) + ((self.chart.config.x.bandwidth() - (self.chart.config.x.bandwidth() / 4))  / self.chart.data.length) * elementIndex
      })
      // .attr('rx', 5)
      // .attr('height', 0)
      .transition().duration(500)
      .attr('width', (self.chart.config.x.bandwidth() - (self.chart.config.x.bandwidth() / 4)) / self.chart.data.length - 5)

      .attr('y', d => self.chart.config.y(Math.max(0,d.value)))
      .attr('height', d => Math.abs(self.chart.config.y(d.value) - self.chart.config.y(0)))


  // colGroups.select('.rect')
  //     .attr('fill', d => d.fillColor)
  //     .transition()
  //     .attr('d', function(d, i, a) {
  //         let periodArray =  newData.filter( obj => obj.period === d.period ).map( obj => obj.municipality.code );
  //         let elementIndex = periodArray.findIndex( o => o == d.municipality.code)
  //         // return self.chart.config.x(d.period) + (self.chart.config.x.bandwidth() / 8) + ((self.chart.config.x.bandwidth() - (self.chart.config.x.bandwidth() / 4))  / self.chart.data.length) * elementIndex

  //         return 'M' + (self.chart.config.x(d.period) + (self.chart.config.x.bandwidth() / 8) + ((self.chart.config.x.bandwidth() - (self.chart.config.x.bandwidth() / 4))  / self.chart.data.length) * elementIndex) + ',' + self.chart.config.y(Math.max(0,d.value)) +
  //         ' v' + (Math.abs(self.chart.config.y(d.value) - self.chart.config.y(0))) + ' q5,0 5,5 h' + ((self.chart.config.x.bandwidth() - (self.chart.config.x.bandwidth() / 4)) / self.chart.data.length - 5) + ' q0,5 -5,5 v-' +  (Math.abs(self.chart.config.y(d.value) - self.chart.config.y(0))) + ' z'


  //     })



    colGroups.select('.label')
      .html(d => `${d.municipality.name} ${d.value}`)
      .attr('x', (d,i,a) => {
        let labelWidth = d3Select(a[i]).node().getBBox().width
        let colWidth = (self.chart.config.x.bandwidth() - (self.chart.config.x.bandwidth() / 4)) / self.chart.data.length
        return self.chart.config.x(d.period) + (colWidth / 2) + (labelWidth / 2)
      })
      .attr('y', function(d) {
        return self.chart.config.y(d.value) - 20
      })
      .attr('fill','#000')
      .attr('opacity', 0)


      if(adjustMedians == true) {
        self.loadMedians(self.chart.medians)
      }


    colGroups.select('.labelBackground')
      .attr('x', (d,i,a) => { return d3Select(a[i].parentNode).select('.label').node().getBBox().x - 8} )
      .attr('y', (d,i,a) => { return d3Select(a[i].parentNode).select('.label').node().getBBox().y - 4 } )
      .attr('fill','#fff')
      .attr('rx', 5)
      .attr('height', (d,i,a) => { return d3Select(a[i].parentNode).select('.label').node().getBBox().height + 8 } )
      .attr('width', (d,i,a) => { return d3Select(a[i].parentNode).select('.label').node().getBBox().width + 16 } )
      .attr('opacity', 0)



  }


  _colMouseOver(d) {

    let allColumns = document.querySelectorAll(this.chart.config.bindto + ' .colGroup')
    allColumns.forEach(el => el.classList.remove('focus'))

    let colId = d.target.parentElement.attributes['colid'].value

    let selectedCols = document.querySelectorAll(this.chart.config.bindto + ' .colGroup[colid="'+colId+'"]')
    selectedCols.forEach(el => el.classList.add('focus'))

  }

  _colMouseOut(d) {

      let allColumns = document.querySelectorAll(this.chart.config.bindto + ' .colGroup')
      allColumns.forEach(el => el.classList.remove('focus'))

  }


  loadMedians(medians, hide = false) {

    let self = this;

    self.chart.medians = medians

    self._adjustY()

    let mediansContainer = d3Select(self.chart.config.bindto + ' .medians')

    let medianLines = mediansContainer.selectAll('.median')
        .data(self.chart.medians)

    medianLines.enter().append('line')
      .attr('class', 'median')
      .attr('stroke','#000')
      .attr('stroke-dasharray','3px')

    medianLines
      .transition()
      .attr("x1", d => self.chart.config.x(d.period))
      .attr("x2", d => self.chart.config.x(d.period) + self.chart.config.x.bandwidth() - 10)
      .attr("y1", d => self.chart.config.y(d.value))
      .attr("y2", d => self.chart.config.y(d.value))
      .attr('opacity', hide == true ? 0 : 1)

    medianLines.exit().remove()

    this.loadData(self.chart.data, false)

  }

  removeMedians() {

    let periodArray = this.chart.data[0].data.map(function(d) { return d.period } )

    let medianArray = []

    periodArray.forEach(p => medianArray.push({period: p, value: 0}))

    this.chart.medians = medianArray

    this.loadMedians(this.chart.medians, true)

  }



  highlightCol(id) {
    let cols = document.querySelectorAll(this.chart.config.bindto + ' g[colid="'+id+'"]')
	  cols.forEach(el => el.classList.add('focus'))
  }


  _loadFilters() {

    let labelBackground = document.createElement('div')
    labelBackground.innerHTML = `
      <svg>
      <defs>
        <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
          <feDropShadow stdDeviation="5" flood-color="#000" flood-opacity="0.5" />
        </filter>
      </defs>
      </svg>`
    document.body.appendChild(labelBackground)



  }

}
