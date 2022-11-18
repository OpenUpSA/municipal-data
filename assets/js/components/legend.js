import { logIfUnequal } from '../utils.js';

export default class LegendItem {
  constructor(template, color, label) {
    this.$element = template.clone();
    logIfUnequal(1, this.$element.length);
    this.$element.find('div:eq(1)').text(label);
    this.$element.find('.legend-block__colour').css('background-color', color);
  }
}
