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
    this.$element.attr("href", url);
  }
}

export class LinkField {
  constructor(selectorOrElement, url, options) {
    this.$element = $(selectorOrElement);
    this.$element.attr("href", url);
    if (options) {
      Object.entries(options).forEach(([key, value]) => {
        this.$element.attr(key, value);
      });
    }
  }
}
