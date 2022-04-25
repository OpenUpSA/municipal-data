import { logIfUnequal, capFirst, formatFinancialYear, ratingColor } from '../utils.js';

class Icon {
  constructor($template, iconClasses, color) {
    this.$element = $template.clone();
    this.$element.removeClass("audit-outcome__icon--green audit-outcome__icon--yellow");
    this.$element.addClass(`audit-outcome__icon--${ color }`);
    this.$element.find("div").attr("class", iconClasses);
  }

  render() {
    return this.$element;
  }
}

class ReportCard {
  constructor($element, key, report) {
    this.$element = $element;
    logIfUnequal(1, this.$element.length);
    this.$element.find(".audit-outcome__year").text(formatFinancialYear(key));
    this.$element.find(".audit-outcome__heading").text(report.result);

    if (report.report_url === null) {
      this.$element.find(".audit-outcome__download").text("No report available");
    }
    else if (report.report_url.endsWith('.pdf')) {
      report.report_url = report.report_url.substring(0, report.report_url.lastIndexOf("/"));
    }

    this.$element.find(".audit-outcome__download").attr("href", report.report_url);

    this.rating = report.rating;
    this.initIcons();
  }

  initIcons() {
    const $iconContainer = this.$element.find(".audit-outcome__icons");
    const $iconTemplate = $iconContainer.find(".audit-outcome__icon").first().clone();
    $iconContainer.empty();

    if (this.rating == "unqualified") {
      $iconContainer.append(new Icon($iconTemplate, "fas fa-thumbs-up", "green").render());
      $iconContainer.append(new Icon($iconTemplate, "fas fa-trophy", "yellow").render());
    } else if (this.rating == "unqualified_emphasis_of_matter") {
      $iconContainer.append(new Icon($iconTemplate, "fas fa-thumbs-up", "green").render());
    } else if (this.rating == "qualified") {
      $iconContainer.append(new Icon($iconTemplate, "fas fa-thumbs-down", "red").render());
    } else if (["adverse", "disclaimer"].includes(this.rating)) {
      $iconContainer.append(new Icon($iconTemplate, "fas fa-exclamation", "red").render());
    } else if (this.rating == "outstanding") {
      $iconContainer.append(new Icon($iconTemplate, "fas fa-clock", "black").render());
    }
    $iconContainer.removeClass("hidden");
  }
}

export class AuditOpinions {
  selector = "#audit-outcomes";

  constructor(reports) {
    this.$element = $(this.selector);
    logIfUnequal(1, this.$element.length);
    // Using Object.entries() and sort() as documenteded here
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries
    // to loop through the reports["values"] objects and order by key
    Object.entries(reports["values"]).sort((a, b) => b[0].localeCompare(a[0])).forEach(([key, value], index) => {
      const $element = this.$element.find(`.audit-outcome:eq(${ index })`);
      new ReportCard($element, key, value);
    });
  }
}
