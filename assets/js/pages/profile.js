import { logIfUnequal, locale, capFirst, formatFinancialYear, ratingColor } from '../utils.js';
import { ContactSection } from '../components/contacts.js';
import { TextField } from '../components/common.js';
import { IndicatorSection, OverUnderSection } from '../components/indicators.js';
import { AuditOpinions } from '../components/audit-opinions.js';
import { ProfileHeader } from '../components/profile-header.js';
import { InPageNav } from '../components/in-page-nav.js';
import { CapitalProjectList } from '../components/capital-projects.js';

export default class ProfilePage {
  constructor(pageData) {
    const maps = new Maps();
    maps.drawMapsForProfile(".profile-map", pageData.geography, pageData.demarcation);

    new ProfileHeader(pageData.geography, pageData.total_population, pageData.population_density);
    new InPageNav(pageData.geography, pageData.total_population, pageData.pdf_url);

    new ContactSection(pageData.muni_contact, pageData.mayoral_staff, pageData.geography);

    new AuditOpinions(pageData.audit_opinions);

    const initSection = (className, selector, key) => {
      new className(
        selector,
        pageData.indicators[key],
        pageData.medians[key],
        pageData.geography,
      );
    };
    initSection(IndicatorSection, "#cash-balance", "cash_at_year_end");
    initSection(IndicatorSection, "#cash-coverage", "cash_coverage");
    initSection(OverUnderSection, "#operating-budget", "op_budget_diff");
    initSection(OverUnderSection, "#capital-budget", "cap_budget_diff");
    initSection(IndicatorSection, "#repairs-maintenance", "rep_maint_perc_ppe");
    initSection(IndicatorSection, "#wasteful-expenditure", "wasteful_exp");
    initSection(IndicatorSection, "#current-ratio", "current_ratio");
    initSection(IndicatorSection, "#liquidity-ratio", "liquidity_ratio");
    initSection(IndicatorSection, "#collection-rate", "current_debtors_collection_rate");
    initSection(IndicatorSection, "#wages-salaries", "expenditure_trends_staff");
    initSection(IndicatorSection, "#contractor-services", "expenditure_trends_contracting");

    new CapitalProjectList(pageData.infrastructure_summary, pageData.geography);

    $("#income-sources .indicator-chart")
      .addClass("chart-container")
      .attr("data-chart", "grouped-bar-revenue_breakdown")
      .attr("data-unit", "currency");
    $("#what-is-money-spent-on .indicator-chart")
      .addClass("chart-container")
      .attr("data-chart", "grouped-bar-expenditure_functional_breakdown")
      .attr("data-unit", "currency");
    new HorizontalGroupedBarChart().discover(pageData);



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
    const householdPercent = pageData.household_percent;

    $("#income-over-time .indicator-metric").hide();

    if (householdPercent.Middle) {
      overall_chart($("#income-over-time .indicator-chart")[0], chartData);

      $("#middle-income-over-time .indicator-metric__value").text(`${householdPercent.Middle}%`);
      const middleContainer = $("#middle-income-over-time .indicator-chart")[0];
      income_chart(middleChartData, middleContainer, yearly_percent['Middle Income Range']);

      $("#affordable-income-over-time .indicator-metric__value").text(`${householdPercent.Affordable}%`);
      const affordableContainer = $("#affordable-income-over-time .indicator-chart")[0];
      income_chart(affordableChartData, affordableContainer, yearly_percent['Affordable Range']);

      $("#indigent-income-over-time .indicator-metric__value").text(`${householdPercent.Indigent}%`);
      const indigentContainer = $("#indigent-income-over-time .indicator-chart")[0];
      income_chart(indigentChartData, indigentContainer, yearly_percent['Indigent HH receiving FBS']);
    } else {
      $("<p>Household bills data not available for this municipality.</p>").insertBefore($("#income-over-time"));
      $("#income-over-time").remove();
      $("#middle-income-over-time").remove();
      $("#affordable-income-over-time").remove();
      $("#indigent-income-over-time").remove();
    }
  }

}
