import { logIfUnequal, formatFinancialYear, ratingColor, formatForType, locale } from '../utils.js';
import PercentageStackedChart  from 'municipal-money-charts/src/components/MunicipalCharts/PercentageStackedChart';
import BarChart  from 'municipal-money-charts/src/components/MunicipalCharts/BarChart';
import OverlayBarChart from 'municipal-money-charts/src/components/MunicipalCharts/OverlayBarChart';

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
    this._initChartData();
    this._initSectionPeriod(this._year);
    this._initChart();
  }

  _initChart() {
    this.chart = new BarChart(this.$chartContainer[0])
      .data(this._chartData[this._year])
      .format(locale.format("$,"));
  }

  _initChartData() {
    const items = this.sectionData.values.filter(item => item.amount_type === "AUDA");
    items.forEach(item => item.color = localColor);
    const yearGroups = _.groupBy(items, "date");
    this._year = _.max(_.keys(yearGroups));
    this._chartData = yearGroups;
  }
}

export class NationalConditionalGrantsSection extends IncomeSection {
  constructor(selector, sectionData) {
    super(selector, sectionData);
    this._initChartData();
    this._initSectionPeriod(this._year);
    this._initChart();
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

      // Add dummy data for missing year groups because chart assumes there's
      // a datum for each series in each item, and shows data in the wrong series
      // when a series is missing from an item
      const grantGroups = _.groupBy(this._chartData[year], "grant.label");
      for (let grantLabel in grantGroups) {
        const typeGroups = _.groupBy(grantGroups[grantLabel], "amount_type.code");
        ["ORGB", "TRFR", "ACT"].forEach((typeCode) => {
          if (!(typeCode in typeGroups)) {
            const fake = {
              "amount_type.code": typeCode,
              "amount.sum": null,
              "grant.label": grantLabel,
              "grant.code": grantGroups[grantLabel][0]["grant.code"],
              "financial_year_end.year": grantGroups[grantLabel][0]["financial_year_end.year"],
            };
            this._chartData[year].push(fake);
          }
        });
      }

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
