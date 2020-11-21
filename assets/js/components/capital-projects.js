export class CapitalProjectList {
  constructor(projectList, projectCount, geography) {
    this.$element = $("#capital-projects");
    this.$element.find(".table__showing-value").text(projectList.length);
    this.$element.find(".table__total-value").text(projectCount);
    const moreUrl = `/infrastructure/projects/?municipality=${encodeURIComponent(geography.short_name)}`;
    this.$element.find(".button__see-more").attr("href", moreUrl);
    this.$element.find(".financial-period").text("2019-2020");

    const tableHeader = this.$element.find(".table-row__header");
    const rowTemplate = this.$element.find("a.table-row--2-col-value-right-with-icon").clone();
    this.$element.find("a.table-row--2-col-value-right-with-icon").remove();

    projectList.reverse();
    projectList.forEach((project) => {
      const row = rowTemplate.clone();
      row.find(".table-row__title").text(project.description);
      row.find(".table-row__value").text(project.expenditure_amount);
      row.attr("href", project.url);
      row.insertAfter(tableHeader);
    });
  }
}
