import {
  logIfUnequal,
  formatFinancialYear,
  ratingColor,
  formatForType,
  locale,
  formatPhase,
  humaniseRand,
} from '../utils.js';
import GroupedBarChart from 'municipal-money-charts/src/components/MunicipalCharts/GroupedBarChart';
import Dropdown from './dropdown.js';
import LegendItem from './legend.js';

const colors = {
  "ORGB": "#91B8C5",
  "ADJB": "#23728B",
  "AUDA": "#54298B",
  "IBY1": "#DADADA",
  "IBY2": "#DADADA",
};

const ordering = [
  "ORGB",
  "ADJB",
  "AUDA",
  "IBY1",
  "IBY2",
];

const comparator = (a, b) => {
  return ordering.indexOf(a["amount_type.code"]) - ordering.indexOf(b["amount_type.code"]);
};

export class TimeSeriesSection {
  constructor(selector, sectionData) {
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.sectionData = sectionData;
    this.$chartContainer = this.$element.find(".indicator-chart");

    this._initChart();
    this._initLegend();
  }

  _initChart() {
    const chartData = this.sectionData.map((d) => {
      d.color = colors[d["amount_type.code"]];
      d.financial_year = formatFinancialYear(d.financial_year);
      return d;
    });
    chartData.sort(comparator);

    this.chart = new GroupedBarChart(this.$chartContainer[0])
      .data(chartData)
      .format(x => humaniseRand(x, false, true))
      .seriesField("budget_phase")
      .groupBars("financial_year");
  }

  _initLegend() {
    const container = this.$element.find(".legend-block__wrapper");
    logIfUnequal(1, container.length);
    const template = this.$element.find(".legend-block");
    template.remove();

    ordering.slice(0, 4).forEach((code) => {
      container.append(new LegendItem(template, colors[code], formatPhase(code)).$element);
    });
    this.$element.find(".indicator-chart__legend").css("display", "block");
  }
}
