import { logIfUnequal } from '../utils.js';

export default class ComparisonMenu {
  constructor(containerSelector) {
    this.$element = $(`${containerSelector} .muni-compare`);
    logIfUnequal(1, this.$element.length);
    // this.$element.click(function(e) { console.log("clicked", e) });
    this.$element.find(".w-dropdown-list a").click((function() {
      // const clickEvent = new Event('click', {bubbles: true});

      // this.$element[0].dispatchEvent(clickEvent);
      this.$element.find(".dropdown-toggle, .w-dropdown-list").removeClass("w--open");
      this.$element.find(".dropdown-toggle").attr("aria-expanded", "false");
      this.$element.find(".dropdown").css("z-index", "");
      $.data(this.$element.find(".dropdown")[0], ".wDropdown").open = false;
    }).bind(this));
  }
}
