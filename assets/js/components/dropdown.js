import { logIfUnequal } from '../utils.js';

export default class DropdownMenu {
  constructor(container, options, initialSelectionLabel) {
    this.$element = $(container).find(".dropdown");
    logIfUnequal(1, this.$element.length);

    this.$optionTemplate = this.$element.find(".w-dropdown-list a").first().clone();
    this.$element.find(".w-dropdown-list a").remove();

    options.forEach(([label, data]) => {
      const option = this.$optionTemplate.clone();
      option.text(label);
      this.$element.find(".dropdown-list").append(option);
      option.click((function(e) {
        const selectedOptionElement = $(e.target);
        const option = selectedOptionElement.data("option");
        this.$element.find(".dropdown__current-select").text(selectedOptionElement.text());

        const selectEvent = new CustomEvent("option-select", {
          bubbles: true,
          detail: data,
        });
        this.$element[0].dispatchEvent(selectEvent);

        // Close a dropdown when one of its options are selected
        this.$element.triggerHandler("w-close.w-dropdown");
      }).bind(this));
    });

    this.$element.find(".dropdown__current-select").text(initialSelectionLabel);
  }
}
