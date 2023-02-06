import { logIfUnequal } from '../utils.js';

export default class ComparisonMenu {
  constructor(containerSelector, key) {
    this.$element = $(`${containerSelector} .muni-compare`);
    logIfUnequal(1, this.$element.length);
    this.$dropdown = this.$element.find('.dropdown');
    logIfUnequal(1, this.$dropdown.length);

    this.$element.find('.w-dropdown-list a[data-option=similar-nearby]').hide();

    this.$element.find('.w-dropdown-list a').click(((e) => {
      const selectedOptionElement = $(e.target);
      const option = selectedOptionElement.data('option');
      this.$element.find('.dropdown__current-select').text(selectedOptionElement.text());

      const selectEvent = new CustomEvent('option-select', {
        bubbles: true,
        detail: { option },
      });
      this.$dropdown[0].dispatchEvent(selectEvent);

      // Close a dropdown when one of its options are selected
      this.$dropdown.triggerHandler('w-close.w-dropdown');

      ga('send', 'event', 'compare-in-chart', `${key} ${option}`);
      gtag('event', 'compare_in_chart', {
        label: `${key} ${option}`,
      });
    }));
  }
}
