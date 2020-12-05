import { logIfUnequal, formatFinancialYear, ratingColor, formatForType, locale } from '../utils.js';
import PercentageStackedChart  from 'municipal-money-charts/src/components/MunicipalCharts/PercentageStackedChart';
import BarChart  from 'municipal-money-charts/src/components/MunicipalCharts/BarChart';

const localColor = "#23728B";
const transfersColor = "#54298B";

class IncomeSection {
  constructor(selector, sectionData) {
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.sectionData = sectionData;
    this.$chartContainer = this.$element.find(".indicator-chart");
  }

  _initSectionPeriod(year) {
    this.$element.find(".section-header__info-right").text(formatFinancialYear(year));
  }
}

export class IncomeSummarySection extends IncomeSection {
  constructor(selector, sectionData) {
    super(selector, sectionData);
    this._initSectionPeriod(this.sectionData.year);
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
        `${ d.label }: ${ formatForType("%", d.percent) } or ${ formatForType("R", d.amount) }`
      ]);
  }

  chartData() {
    return [
      {
        "label": "Locally generated",
        "amount": this.sectionData.local.amount,
        "percent": this.sectionData.local.percent,
        "color": localColor,
      },
      {
        "label": "Locally generated",
        "amount": this.sectionData.government.amount,
        "percent": this.sectionData.government.percent,
        "color": transfersColor,
      }
    ];
  }
}

export class LocalIncomeSourcesSection extends IncomeSection {
  constructor(selector, sectionData) {

    super(selector, sectionData);
    this._initChartData();
    this._initSectionPeriod(this._year);
    this._initChart();
  }

  _initChart() {
    this.chart = new BarChart(this.$chartContainer[0]);
    this.chart.data(this._chartData)
      .format(locale.format("$,"));
  }

  _initChartData() {
    const items = this.sectionData.values.filter(item => item.amount_type === "AUDA");
    items.forEach(item => item.color = localColor);
    const yearGroups = _.groupBy(items, "date");
    this._year = _.max(_.keys(yearGroups));
    this._chartData = yearGroups[this._year];
  }
}
