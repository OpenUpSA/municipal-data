import { logIfUnequal, locale, capFirst, formatFinancialYear, ratingColor } from './utils.js';
import { ContactSection } from './components/contacts.js';
import { TextField } from './components/common.js';
import { AnnualSection, QuarterlySection, OverUnderSection } from './components/indicators.js';
import { AuditOpinions } from './components/audit-opinions.js';
import { ProfileHeader } from './components/profile-header.js';
import { InPageNav } from './components/in-page-nav.js';

class ProfilePage {
  constructor() {
    const pageData = JSON.parse(document.getElementById('page-data').textContent);

    const maps = new Maps();
    maps.drawMapsForProfile(pageData.geography, pageData.demarcation);

    new ProfileHeader(pageData.geography, pageData.total_population, pageData.population_density);
    new InPageNav(pageData.geography, pageData.pdf_url);

    const municipality = {
      code: pageData.geography.geo_code,
      name: pageData.geography.short_name,
    };

    const initSection = (className, selector, key) => {
      new className(
        selector,
        pageData.indicators[key],
        pageData.medians[key],
        municipality
      );
    };
    initSection(AnnualSection, "#cash-balance", "cash_at_year_end");
    initSection(AnnualSection, "#cash-coverage", "cash_coverage");
    initSection(OverUnderSection, "#operating-budget", "op_budget_diff");
    initSection(OverUnderSection, "#capital-budget", "cap_budget_diff");
    initSection(AnnualSection, "#repairs-maintenance", "rep_maint_perc_ppe");
    initSection(AnnualSection, "#wasteful-expenditure", "wasteful_exp");
    initSection(QuarterlySection, "#current-ratio", "current_ratio");
    initSection(QuarterlySection, "#liquidity-ratio", "liquidity_ratio");
    initSection(QuarterlySection, "#collection-rate", "current_debtors_collection_rate");
    initSection(AnnualSection, "#wages-salaries", "expenditure_trends_staff");
    initSection(AnnualSection, "#contractor-services", "expenditure_trends_contracting");




    new ContactSection(pageData.mayoral_staff);

    new AuditOpinions(pageData.audit_opinions);

    this.initHouseholdBills(pageData);

    // track outbound links
    $('a[href^=http]').on('click', function(e) {
      ga('send', 'event', 'outbound-click', e.target.href);
    });

  }

  initHouseholdBills(pageData) {
    var yearly_percent = pageData.yearly_percent;
    var chartData = pageData.household_chart_overall;
    var middleChartData = pageData.household_chart_middle;
    var affordableChartData = pageData.household_chart_affordable;
    var indigentChartData = pageData.household_chart_indigent;

    $("#income-over-time .indicator-metric").hide();
    overall_chart($("#income-over-time .indicator-chart")[0], chartData);

    $("#middle-income-over-time .indicator-metric").hide();
    const middleContainer = $("#middle-income-over-time .indicator-chart")[0];
    income_chart(middleChartData, middleContainer, yearly_percent['Middle Income Range']);

    $("#affordable-income-over-time .indicator-metric").hide();
    const affordableContainer = $("#affordable-income-over-time .indicator-chart")[0];
    income_chart(affordableChartData, affordableContainer, yearly_percent['Affordable Range']);

    $("#indigent-income-over-time .indicator-metric").hide();
    const indigentContainer = $("#indigent-income-over-time .indicator-chart")[0];
    income_chart(indigentChartData, indigentContainer, yearly_percent['Indigent HH receiving FBS']);
  }

}

$(function() {
  new ProfilePage();

  // Re-initialise webflow interactions so that cloned elements respond to interactions
  Webflow.require('ix2').init();
});
