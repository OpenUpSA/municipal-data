import { logIfUnequal, capFirst, formatFinancialYear, ratingColor } from '../utils.js';

class Icon {
  constructor($template, iconClasses, color) {
    this.$element = $template.clone();
    this.$element.removeClass("audit-outcome__icon--green audit-outcome__icon--yellow");
    this.$element.addClass(`audit-outcome__icon--${ color }`);
  }

  render() {
    return this.$element;
  }
}

class ReportCard {
  constructor($element, report) {
    this.$element = $element;
    logIfUnequal(1, this.$element.length);
    this.$element.find(".audit-outcome__year").text(formatFinancialYear(report.date));
    this.$element.find(".audit-outcome__heading").text(report.result);
    this.$element.find(".audit-outcome__download").attr("href", report.report_url);
    if (report.report_url) {
    }

    this.rating = report.rating;
    this.initIcons();
  }

  initIcons() {
    const $iconContainer = this.$element.find(".audit-outcome__icons");
    const $iconTemplate = $iconContainer.find(".audit-outcome__icon").first().clone();
    $iconContainer.empty();

    if (this.rating == "unqualified") {
      //   thumbs-up, cup
      $iconContainer.append(new Icon($iconTemplate, "thumbs-up", "green").render());
      $iconContainer.append(new Icon($iconTemplate, "trophy", "yellow").render());
    } else if (this.rating == "unqualified_emphasis_of_matter") {
      // unqualified_emphasis_of_matter
      //   thumbs-up
      $iconContainer.append(new Icon($iconTemplate, "thumbs-up", "green").render());
    } else if (this.rating == "unqualified") {

      // qualified
      //   thumbs-down
      $iconContainer.append(new Icon($iconTemplate, "thumbs-down", "green").render());
    } else if (this.rating == "unqualified") {

      // adverse
      // disclaimer
      //   exclamation-mark
      $iconContainer.append(new Icon($iconTemplate, "exclamation-mark", "green").render());
    } else if (this.rating == "unqualified") {
      // outstanding
      //   clock
      $iconContainer.append(new Icon($iconTemplate, "clock", "green").render());
    }
    $iconContainer.removeClass("hidden");
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
