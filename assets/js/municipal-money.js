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

class TextField {
  constructor(selector, value) {
    this.element = $(selector);
    logIfUnequal(1, this.element.length);
    this.element.text(value);
  }
}

const pageData = JSON.parse(document.getElementById('page-data').textContent);

new TextField(".page-heading__title", pageData.geography.short_name);
new TextField(".profile-metric__population", D3_LOCALE.format(",")(pageData.total_population));
new TextField(".profile-metric__size", D3_LOCALE.format(",.1f")(pageData.geography.square_kms));
new TextField(".profile-metric__density", D3_LOCALE.format(",.1f")(pageData.population_density));
