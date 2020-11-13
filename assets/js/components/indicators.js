import { logIfUnequal, formatFinancialYear, ratingColor, formatForType } from '../utils.js';


const indicatorMetricClass = {
  "good": ".indicator-metric--status-green",
  "ave": ".indicator-metric--status-yellow",
  "bad": ".indicator-metric--status-red",
};

class IndicatorSection {
  constructor(selector, sectionData, municipality) {
    this.selector = selector;
    this.sectionData = sectionData;
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.latestItem = sectionData.values[0];
    this.$element.find(".section-header__info-right").text(formatFinancialYear(this.latestItem.date));
    this.municipality = municipality;
    console.debug(`\n${selector}\n\n\`\`\`json\n${JSON.stringify(this.chartData(), null, 2)}\n\`\`\`\n`);
    this.initMetric();
  }

  formatMetric(value) {
    return formatForType(this.sectionData.result_type, value);
  }

  initMetric() {
    const skeleton = this.$element.find(".indicator-metric");
    const templateClass = indicatorMetricClass[this.latestItem.rating];
    const $element = $(`.components ${templateClass}`).clone();
    const value = this.formatMetric(this.latestItem.result);
    $element.find(".indicator-metric__value").text(value);
    skeleton.hide();
    $element.insertBefore(skeleton);
    skeleton.remove();
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
