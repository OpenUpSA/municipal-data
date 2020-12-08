import { logIfUnequal, formatFinancialYear, ratingColor, formatForType, locale } from '../utils.js';
import PercentageStackedChart  from 'municipal-money-charts/src/components/MunicipalCharts/PercentageStackedChart';
import BarChart  from 'municipal-money-charts/src/components/MunicipalCharts/BarChart';
import OverlayBarChart from 'municipal-money-charts/src/components/MunicipalCharts/OverlayBarChart';
import Dropdown from './dropdown.js';

const localColor = "#23728B";
const transfersColor = "#54298B";
const transferredColor = "#A26CE8";
const spentColor = "#91899C";

class IncomeSection {
  constructor(selector, sectionData) {
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.sectionData = sectionData;
    this.$chartContainer = this.$element.find(".indicator-chart");
  }

}

export class IncomeSummarySection extends IncomeSection {
  constructor(selector, sectionData) {
    super(selector, sectionData);
    this._initIndicator();
    this._initChart();
  }

  _initIndicator() {
    const value = this.sectionData["government"].amount + this.sectionData["local"].amount;
    this.$element.find(".indicator-metric__value").text(formatForType("R", value));
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
        "label": "Transfers",
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
    this._initIndicator();
    this._initChartData();
    this._initChart();
    this._initLegend();
  }

  _initIndicator() {
    const value = this.sectionData.revenueSources["local"].amount;
    this.$element.find(".indicator-metric__value").text(formatForType("R", value));
  }

  _initChart() {
    this.chart = new BarChart(this.$chartContainer[0])
      .data(this._chartData[this._year])
      .format(locale.format("$,"));
  }

  _initLegend() {
    this.$element.find(".legend-block div:eq(1)").text("Amount received");
    this.$element.find(".legend-block__colour").css("background-color", localColor);
    this.$element.find(".indicator-chart__legend").css("display", "block");
  }

  _initChartData() {
    const items = this.sectionData.revenueBreakdown.values.filter(item => item.amount_type === "AUDA");
    items.forEach(item => item.color = localColor);
    const yearGroups = _.groupBy(items, "date");
    this._year = _.max(_.keys(yearGroups));
    this._chartData = yearGroups;
  }
}

export class LegendItem {
  constructor(template, color, label) {
    this.$element = template.clone();
    logIfUnequal(1, this.$element.length);
    this.$element.find("div:eq(1)").text(label);
    this.$element.find(".legend-block__colour").css("background-color", color);
  }
}

export class NationalConditionalGrantsSection extends IncomeSection {
  constructor(selector, sectionData) {
    super(selector, sectionData);
    this._initChartData();
    this._initChart();
    this._initLegend();
  }

  _initLegend() {
    const container = this.$element.find(".legend-block__wrapper");
    logIfUnequal(1, container.length);
    const template = this.$element.find(".legend-block");
    template.remove();
    container.append(new LegendItem(template, transfersColor, "Budgeted amount").$element);
    container.append(new LegendItem(template, transferredColor, "Amount transferred up to ").$element);
    container.append(new LegendItem(template, spentColor, "Amount spent up to ").$element);
    this.$element.find(".indicator-chart__legend").css("display", "block");
  }

  _initChart() {
    this.chart = new OverlayBarChart(this.$chartContainer[0])
      .data(this._chartData[this._year])
      .seriesOrder(this._seriesOrder)
      .width(this.$chartContainer.width())
      .format(locale.format("$,"));
  }

  _initChartData() {
    this._chartData = this.sectionData.national_conditional_grants;

    for (let year in this._chartData) {
      // Map keys to the keys assumed by the chart
      this._chartData[year].forEach((item) => {
        item.item = item["grant.label"];
        delete item["grant.label"];
        item.amount = item["amount.sum"];
        delete item["amount.sum"];

        switch (item["amount_type.code"]) {
        case "ORGB":
          item.phase = "Amount budgeted";
          break;
        case "TRFR":
          item.phase = "Transferred up to";
          break;
        case "ACT":
          item.phase = "Spent up to";
        }
      });
    }
    this._seriesOrder = ["Amount budgeted", "Transferred up to", "Spent up to"] ;
    this._year = _.max(_.keys(this._chartData));
  }
}

export class ProvincialTransfersSection extends IncomeSection {
  constructor(selector, sectionData) {
    super(selector, sectionData);
    this._initChartData();
    this._initChart();
    this._initLegend();
    const initialPeriodOption = this._initDropdown();
    this.selectData(initialPeriodOption[1]);
  }

  _initChart() {
    this.chart = new BarChart(this.$chartContainer[0])
      .format(locale.format("$,"));
  }

  _initLegend() {
    this.$element.find(".legend-block div:eq(1)").text("Amount budgeted");
    this.$element.find(".legend-block__colour").css("background-color", transfersColor);
    this.$element.find(".indicator-chart__legend").css("display", "block");
  }

  _initChartData() {
    const years = this.sectionData.provincial_transfers;
    this._chartData = {};
    for (let year in years) {
      this._chartData[year] = _.groupBy(years[year], "amount_type.code");

      years[year].forEach(item => {
        item.color = transfersColor;
        item.amount = item["amount.sum"];
        delete item["amount.sum"];
        item.item = item["grant.label"];
        delete item["grant.label"];
      });
    }
    this._year = _.max(_.keys(this._chartData));
  }

  _initDropdown() {
    const options = [];
    for (let year in this._chartData) {
      for (let phase in this._chartData[year]) {
        options.push([`${formatFinancialYear(year)} ${phase}`, {
          year: year,
          phase: phase,
        }]);
      }
    }
    options.reverse();

    const initialOption = options[0];
    this.dropdown = new Dropdown(this.$element.find(".fy-select"), options, initialOption[0]);
    this.dropdown.$element.on("option-select", (e) => this.selectData(e.detail));
    return initialOption;
  }

  selectData(selection) {
    this.chart.data(this._chartData[selection.year][selection.phase]);
  }
}
