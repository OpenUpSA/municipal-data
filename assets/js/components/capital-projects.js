import { logIfUnequal, formatFinancialYear, formatForType } from '../utils.js';

export class CapitalProjectList {
  constructor(infrastructure, geography) {
    this.$element = $('#capital-projects');
    this.$element.find('.table__showing-value').text(infrastructure.projects.length);
    this.$element.find('.table__total-value').text(infrastructure.project_count);
    const moreUrl = `/infrastructure/projects/?municipality=${encodeURIComponent(geography.short_name)}`;
    this.$element.find('.button__see-more').attr('href', moreUrl);
    this.$element.find('.financial-period').text(formatFinancialYear(infrastructure.financial_year));

    const tableHeader = this.$element.find('.table-row__header');
    const rowTemplate = this.$element.find('a.table-row--2-col-value-right-with-icon').clone();
    this.$element.find('a.table-row--2-col-value-right-with-icon').remove();

    infrastructure.projects.reverse();
    infrastructure.projects.forEach((project) => {
      const row = rowTemplate.clone();
      row.find('.table-row__title').text(project.description);
      row.find('.table-row__value').text(formatForType('R', project.expenditure_amount));
      row.attr('href', project.url);
      row.insertAfter(tableHeader);
    });
    this.$element.find('.video_download-button').attr('href', '/help#municipal-budget-video');
  }
}
