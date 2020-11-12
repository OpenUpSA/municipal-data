import { logIfUnequal } from '../utils.js';

export class TextField {
  constructor(selector, value) {
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.$element.text(value);
  }
}
