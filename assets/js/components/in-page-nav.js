import { logIfUnequal, locale, capFirst } from '../utils.js';
import { TextField, LinkedTextField, LinkField } from './common.js';

export class InPageNav {
  constructor(geography, pdfUrl) {
    this.$element = $(".page-nav");

    // new TextField(".page-heading__title", geography.short_name);

    const tweetQueryParams = new URLSearchParams([
      ["url", window.location],
      ["related", "MoneyMunicipal"],
    ]);
    const tweetUrl = `https://twitter.com/share?${ tweetQueryParams.toString() }`;
    new LinkField(".page-options__link-share-twitter", tweetUrl, {target: "_blank"});
    new LinkField(".page-options__link-download-pdf", pdfUrl);
  }
}
