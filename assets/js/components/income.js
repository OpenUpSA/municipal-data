import { logIfUnequal, formatFinancialYear, ratingColor, formatForType } from '../utils.js';
import PercentageStackedChart  from 'municipal-money-charts/src/components/MunicipalCharts/PercentageStackedChart';

export class IncomeSummarySection {
  constructor(selector, sectionData) {
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.sectionData = sectionData;
    this.$chartContainer = this.$element.find(".indicator-chart");

    this._initSectionPeriod();
    this._initChart();
  }

  _initChart() {
    this.chart = new PercentageStackedChart(this.$chartContainer[0]);
    this.chart.data(this.chartData())
      .mainLabel((d) => [
        formatForType("%", d.percent),
        formatForType("R", d.amount),
      ])
      .subLabel((d) => [
        `${ d.label }: ${ formatForType("R", d.amount) }`
      ]);
  }

  chartData() {
    return [
      {
        "label": "Locally generated",
        "amount": this.sectionData.local.amount,
        "percent": this.sectionData.local.percent,
        "color": "#23728B",
      },
      {
        "label": "Locally generated",
        "amount": this.sectionData.government.amount,
        "percent": this.sectionData.government.percent,
        "color": "#54298B",
      }
    ];
  }

  _initSectionPeriod() {
    this.$element.find(".section-header__info-right").text(formatFinancialYear(this.sectionData.year));
  }

}
