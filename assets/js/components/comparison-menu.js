import { logIfUnequal } from '../utils.js';

export default class ComparisonMenu {
  constructor(containerSelector) {
    this.$element = $(`${containerSelector} .muni-compare`);
    logIfUnequal(1, this.$element.length);
    this.$dropdown = this.$element.find(".dropdown");
    logIfUnequal(1, this.$dropdown.length);

    this.$element.find(".w-dropdown-list a").click((function(e) {
      const selectedOptionElement = $(e.target);
      this.$element.find(".dropdown__current-select").text(selectedOptionElement.text());

      const selectEvent = new CustomEvent("option-select", {
        bubbles: true,
        detail: {option: selectedOptionElement.data("option")}
      });
      this.$dropdown[0].dispatchEvent(selectEvent);

      // Close a dropdown when one of its options are selected
      this.$dropdown.triggerHandler("w-close.w-dropdown");
    }).bind(this));
  }


}
