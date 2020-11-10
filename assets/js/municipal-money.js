import { formatLocale } from 'd3-format';

var D3_LOCALE = formatLocale({
  decimal: ".",
  thousands: " ",
  grouping: [3],
  currency: ["R", ""],
});

function logIfUnequal(a, b) {
  if (a !== b) {
    console.error(`${a} !== ${b}`);
  }
}

function capFirst(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

class TextField {
  constructor(selector, value) {
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.$element.text(value);
  }
}

const pageData = JSON.parse(document.getElementById('page-data').textContent);

new TextField(".page-heading__title", pageData.geography.short_name);
new TextField(".profile-metric__population", D3_LOCALE.format(",")(pageData.total_population));
new TextField(".profile-metric__size", D3_LOCALE.format(",.1f")(pageData.geography.square_kms));
new TextField(".profile-metric__density", D3_LOCALE.format(",.1f")(pageData.population_density));

new TextField(".page-heading__muni-type", capFirst(pageData.geography.category_name));

const ancestors = pageData.geography.ancestors;
if (ancestors.length) {
  const geoParent1 = new TextField(".page-heading__geo-parent-1", ancestors[0].short_name);
  const url = `/profiles/${ ancestors[0].full_geoid }-${ ancestors[0].slug }`;
  geoParent1.$element.parent().attr("href", url);
}

new TextField(".page-heading__geo-parent-2", pageData.geography.province_name);

function formatFinancialYear(financialYearEnd) {
  return `${ financialYearEnd - 1 }-${ financialYearEnd }`;
}

function ratingColor(rating) {
  return {
    "good": "#34A853",
    "ave": "#FBBC05",
    "bad": "#F00",
  }[rating];
}

class Section {
  constructor(selector, sectionData, municipality) {
    this.selector = selector;
    this.sectionData = sectionData;
    this.$element = $(selector);
    const latestItem = sectionData.values[0];
    this.$element.find(".section-header__info-right").text(latestItem.date);
    console.log(`\n${selector}\n\n\`\`\`json\n${JSON.stringify(this.chartData(), null, 2)}\n\`\`\``);
  }

  chartData() {
    const items = this.sectionData.values.map((item) => {
      return {
        period: formatFinancialYear(item.date),
        fillColor: ratingColor(item.rating),
        value: item.result,
      };
    });
    items.reverse();
    return {
      municipality: municipality,
      data: items,
    };
  }
}

const municipality = {
  code: pageData.geography.geo_code,
  name: pageData.geography.short_name,
};

new Section("#cash-balance", pageData.indicators.cash_at_year_end, municipality);
new Section("#cash-coverage", pageData.indicators.cash_coverage, municipality);
new Section("#operating-budget", pageData.indicators.op_budget_diff, municipality);
new Section("#capital-budget", pageData.indicators.cap_budget_diff, municipality);
new Section("#repairs-maintenance", pageData.indicators.rep_maint_perc_ppe, municipality);
new Section("#wasteful-expenditure", pageData.indicators.wasteful_exp, municipality);
new Section("#current-ratio", pageData.indicators.current_ratio, municipality);
new Section("#liquidity-ratio", pageData.indicators.liquidity_ratio, municipality);
