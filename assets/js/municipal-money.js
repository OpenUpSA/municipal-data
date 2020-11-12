import { logIfUnequal, locale, capFirst, formatFinancialYear, ratingColor } from './utils.js';
import { ContactSection } from './components/contacts.js';
import { TextField } from './components/common.js';
import { AnnualSection, QuarterlySection } from './components/indicators.js';

const pageData = JSON.parse(document.getElementById('page-data').textContent);

new TextField(".page-heading__title", pageData.geography.short_name);
new TextField(".profile-metric__population", locale.format(",")(pageData.total_population));
new TextField(".profile-metric__size", locale.format(",.1f")(pageData.geography.square_kms));
new TextField(".profile-metric__density", locale.format(",.1f")(pageData.population_density));

new TextField(".page-heading__muni-type", capFirst(pageData.geography.category_name));

const ancestors = pageData.geography.ancestors;
if (ancestors.length) {
  const geoParent1 = new TextField(".page-heading__geo-parent-1", ancestors[0].short_name);
  const url = `/profiles/${ ancestors[0].full_geoid }-${ ancestors[0].slug }`;
  geoParent1.$element.parent().attr("href", url);
}

new TextField(".page-heading__geo-parent-2", pageData.geography.province_name);

const municipality = {
  code: pageData.geography.geo_code,
  name: pageData.geography.short_name,
};

new AnnualSection("#cash-balance", pageData.indicators.cash_at_year_end, municipality);
new AnnualSection("#cash-coverage", pageData.indicators.cash_coverage, municipality);
new AnnualSection("#operating-budget", pageData.indicators.op_budget_diff, municipality);
new AnnualSection("#capital-budget", pageData.indicators.cap_budget_diff, municipality);
new AnnualSection("#repairs-maintenance", pageData.indicators.rep_maint_perc_ppe, municipality);
new AnnualSection("#wasteful-expenditure", pageData.indicators.wasteful_exp, municipality);
new QuarterlySection("#current-ratio", pageData.indicators.current_ratio, municipality);
new QuarterlySection("#liquidity-ratio", pageData.indicators.liquidity_ratio, municipality);


new ContactSection(pageData.mayoral_staff);

// Re-initialise webflow interactions so that cloned elements respond to interactions
Webflow.require('ix2').init();
