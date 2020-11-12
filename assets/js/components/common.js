import { logIfUnequal } from '../utils.js';

export class TextField {
  constructor(selectorOrElement, value) {
    this.$element = $(selectorOrElement);
    logIfUnequal(1, this.$element.length);
    this.$element.text(value);
  }
}

export class LinkedTextField extends TextField {
  constructor(selectorOrElement, value, url) {
    super(selectorOrElement, value);
    this.$element.parent().attr("href", url);
  }
}
