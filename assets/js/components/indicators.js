import { logIfUnequal, formatFinancialYear, ratingColor } from '../utils.js';


class IndicatorSection {
  constructor(selector, sectionData, municipality) {
    this.selector = selector;
    this.sectionData = sectionData;
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    const latestItem = sectionData.values[0];
    this.$element.find(".section-header__info-right").text(latestItem.date);
    this.municipality = municipality;
    console.debug(`\n${selector}\n\n\`\`\`json\n${JSON.stringify(this.chartData(), null, 2)}\n\`\`\`\n`);
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
    return D3_LOCALE.format(this.formatSpecifier())(value);
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
