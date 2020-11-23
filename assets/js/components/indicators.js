import { logIfUnequal, formatFinancialYear, ratingColor, formatForType } from '../utils.js';
import { ColumnChart } from './charts/column.js';

const indicatorMetricClass = {
  "good": ".indicator-metric--status-green",
  "ave": ".indicator-metric--status-yellow",
  "bad": ".indicator-metric--status-red",
  "": ".indicator-metric--no-status",
};

function comparePeriod( a, b ) {
  if ( a.period < b.period ){
    return -1;
  }
  if ( a.period > b.period ){
    return 1;
  }
  return 0;
}

export class IndicatorSection {
  constructor(selector, sectionData, medians, geography) {
    this.selector = selector;
    this.sectionData = sectionData;
    this.medians = medians;
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.latestItem = sectionData.values[0];

    this.geography = geography;

    const chartContainerSelector = `${selector} .indicator-chart`;
    this.chart = new ColumnChart(chartContainerSelector, [this.chartData()]);
    const chartContainerParent = $(chartContainerSelector).parent();

    const $provinceButton = $("<button></button>");
    $provinceButton.text(` in ${geography.province_name}`);
    $provinceButton.on("click", (function() {
      this.chart.loadMedians(this.formatMedians().provincial);
    }).bind(this));

    const $nationalButton = $("<button>nationally</button>");
    $nationalButton.on("click", (function() {
      this.chart.loadMedians(this.formatMedians().national);
    }).bind(this));


    const averageControls = $("<p></p>");
    averageControls.append('Show average for <a href="/help">similar municipalities</a>');
    if (geography.category_name !== "metro municipality") {
      averageControls.append([
        $provinceButton,
        " or"
      ]);
    }
    averageControls.append($nationalButton);
    chartContainerParent.append(averageControls);


    this.initSectionPeriod();
    this.initMetric();
  }

  formatMetric(value) {
    return formatForType(this.sectionData.result_type, value);
  }

  initSectionPeriod() {
    this.$element.find(".section-header__info-right").text(this.formatPeriod(this.latestItem.date));
  }

  initMetric() {
    const $skeleton = this.$element.find(".indicator-metric");
    logIfUnequal(1, $skeleton.length);
    const templateClass = indicatorMetricClass[this.latestItem.rating];
    const $element = $(`.components ${templateClass}`).clone();
    logIfUnequal(1, $element.length);
    const value = this.formatMetric(this.latestItem.result);
    $element.find(".indicator-metric__value").text(value);
    $skeleton.hide();
    $element.insertBefore($skeleton);
    $skeleton.remove();
  }

  chartData() {
    const items = this.sectionData.values.map((item) => {
      return {
        period: this.formatPeriod(item.date),
        fillColor: ratingColor(item.rating),
        value: item.result,
      };
    });
    items.reverse();
    return {
      municipality: {
        code: this.geography.geo_code,
        name: this.geography.short_name,
      },
      data: items,
      resultType: this.resultType(),
    };
  }

  formatMedians() {
    const national = Object.entries(this.medians.national.dev_cat).map(([key, value]) => {
      return {
        period: this.formatPeriod(key),
        value: value,
      };});
    const provincial = Object.entries(this.medians.provincial.dev_cat).map(([key, value]) => {
      return {
        period: this.formatPeriod(key),
        value: value,
      };});
    national.sort(comparePeriod);
    provincial.sort(comparePeriod);
    return {
      national: national,
      provincial: provincial,
    };
  }

  resultType() {
    return {
      "R": "currency",
      "%": "percentage",
    }[this.sectionData.result_type] || this.sectionData.result_type;
  }

  formatSpecifier() {
    return {
      "R": "$,.0f",
    }[this.sectionData.result_type];
  }

  formatValue(value) {
    return locale.format(this.formatSpecifier())(value);
  }

  formatPeriod(period) {
    return formatFinancialYear(period);
  }
}

export class OverUnderSection extends IndicatorSection {
  formatMetric(value) {
    const overunder = value > 0 ? "overspent" : "underspent";
    return `${super.formatMetric(value)} ${overunder}`;
  }
}
