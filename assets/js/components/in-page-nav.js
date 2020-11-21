import { logIfUnequal, locale, capFirst } from '../utils.js';
import { TextField, LinkedTextField, LinkField } from './common.js';

export class InPageNav {
  constructor(geography, pdfUrl) {
    this.$element = $(".page-nav");

    // new TextField(".page-heading__title", geography.short_name);
    new LinkField(".page-options__link-download-pdf", pdfUrl);
  }
}
