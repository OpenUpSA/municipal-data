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

class IndicatorSection {
  constructor(selector, sectionData, medians, municipality) {
    this.selector = selector;
    this.sectionData = sectionData;
    this.medians = medians;
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.latestItem = sectionData.values[0];

    this.municipality = municipality;

    const chartContainerSelector = `${selector} .indicator-chart`;
    this.chart = new ColumnChart(chartContainerSelector, [this.chartData()]);
    const chartContainerParent = $(chartContainerSelector).parent();

    const $provinceButton = $("<button>in province</button>");
    $provinceButton.on("click", (function() {
      this.chart.removeMedians();
      this.chart.loadMedians(this.formatMedians().provincial);
    }).bind(this));

    const $nationalButton = $("<button>nationally</button>");
    $nationalButton.on("click", (function() {
      this.chart.removeMedians();
      this.chart.loadMedians(this.formatMedians().national);
    }).bind(this));

    chartContainerParent.append(
      $("<p></p>").append([
        "Show average for similar municipalities",
        $provinceButton,
        $nationalButton,
      ])
    );


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
      municipality: this.municipality,
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
}

export class AnnualSection extends IndicatorSection {
  formatPeriod(period) {
    return formatFinancialYear(period);
  }
}

export class QuarterlySection extends IndicatorSection {
  formatPeriod(period) {
    return period;
  }
}

export class OverUnderSection extends AnnualSection {
  formatMetric(value) {
    const overunder = value > 0 ? "overspent" : "underspent";
    return `${super.formatMetric(value)} ${overunder}`;
  }
}
