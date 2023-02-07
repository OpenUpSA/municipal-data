import { logIfUnequal, capFirst, formatFinancialYear, ratingColor } from '../utils.js';

class Icon {
  constructor($template, iconClasses, color) {
    this.$element = $template.clone();
    this.$element.removeClass("audit-outcome__icon--green audit-outcome__icon--yellow");
    this.$element.addClass(`audit-outcome__icon--${color}`);
    this.$element.find("div").attr("class", iconClasses);
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

    let reportURL = report.report_url;
    if (!reportURL) {
      this.$element.find(".audit-outcome__download").text("No report available");
    }
    else if (!reportURL.startsWith('https') && reportURL.endsWith('.pdf')) {
      reportURL = reportURL.substring(0, reportURL.lastIndexOf("/"));
      this.$element.find(".audit-outcome__download").attr("href", reportURL);
    }
    else {
      this.$element.find(".audit-outcome__download").attr("href", reportURL);
    }
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
    reports.values.forEach((report, index) => {
      const $element = this.$element.find(`.audit-outcome:eq(${index})`);
      new ReportCard($element, report);
    });

    $(`${this.selector} .expand-block`).on('click', ((e) => {
      gtag('event', 'about_indicator', {
        category: "More info",
        action: "Expand",
        label: `audit-outcomes ${$(e.target).text()}`,
      });
    }));
  }
}
