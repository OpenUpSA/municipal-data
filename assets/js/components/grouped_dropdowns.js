export default class DropdownMenu {
  constructor(dropdown, options, initialSelection, linkedInitialSelection, linkedDropdown) {
    this.$element = $(dropdown);
    this.$linkedElement = $(linkedDropdown);

    this.$optionTemplate = this.$element.find('.w-dropdown-list a').first().clone();
    this.$linkedOptionTemplate = this.$linkedElement.find('.w-dropdown-list a').first().clone();
    this.$element.find('.w-dropdown-list a').remove();
    this.$linkedElement.find('.w-dropdown-list a').remove();

    options.forEach(([label, data]) => {
      const option = this.$optionTemplate.clone();
      option.text(label);
      this.$element.find('.dropdown-list').append(option);
      option.click(((e) => {
        const selectedOptionElement = $(e.target);
        //const option = selectedOptionElement.data('option');
        this.$element.find('.dropdown__current-select').text(selectedOptionElement.text());
        const selectEvent = new CustomEvent('option-select', {
          bubbles: true,
          detail: data[Object.keys(data)[0]],
        });
        this.$element[0].dispatchEvent(selectEvent);
        // Update linked dropdown
        this.updateLinkedDropdown(label, data, label);
        // Close a dropdown when one of its options are selected
        this.$element.triggerHandler('w-close.w-dropdown');
      }));
      this.updateLinkedDropdown(label, data, initialSelection);
    });
    this.$element.find('.dropdown__current-select').text(initialSelection);
    this.$linkedElement.find('.dropdown__current-select').text(linkedInitialSelection);
  }

  updateLinkedDropdown(label, data, selection) {
    if (selection == label) {
      let initialSelection = Object.keys(data)[0];
      this.$linkedElement.find('.w-dropdown-list a').remove();
      $.each(data, (index, video) => {
        const linkedOption = this.$linkedOptionTemplate.clone();
        linkedOption.text(index);
        this.$linkedElement.find('.dropdown-list').append(linkedOption);
        linkedOption.click(((e) => {
          const linkedSelectedOptionElement = $(e.target);
          //const linkedOption = linkedSelectedOptionElement.data('option');
          this.$linkedElement.find('.dropdown__current-select').text(linkedSelectedOptionElement.text());
          const linkedSelectEvent = new CustomEvent('option-select', {
            bubbles: true,
            detail: data[$(e.target).text()],
          });
          this.$linkedElement[0].dispatchEvent(linkedSelectEvent);
          // Close a dropdown when one of its options are selected
          this.$linkedElement.triggerHandler('w-close.w-dropdown');
        }));
      });
      this.$linkedElement.find('.dropdown__current-select').text(initialSelection);
    }
  }
}
