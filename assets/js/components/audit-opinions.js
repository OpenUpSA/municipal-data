import { logIfUnequal, capFirst, formatFinancialYear, ratingColor } from '../utils.js';

class ReportCard {
  constructor($element, report) {
    this.$element = $element;
    logIfUnequal(1, this.$element.length);
    this.$element.find(".audit-outcome__year").text(formatFinancialYear(report.date));
  }
}

export class AuditOpinions {
  selector = "#audit-outcomes";

  constructor(reports) {
    this.$element = $(this.selector);
    logIfUnequal(1, this.$element.length);

    reports.values.forEach((report, index) => {
      const $element = this.$element.find(`.audit-outcome:eq(${ index })`);
      new ReportCard($element, report);
    });
  }
}
