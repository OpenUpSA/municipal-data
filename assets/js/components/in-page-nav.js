import { logIfUnequal, locale, capFirst } from '../utils.js';
import { TextField, LinkedTextField, LinkField } from './common.js';

export class InPageNav {
  constructor(geography, pdfUrl) {
    this.$element = $(".page-nav");

    // new TextField(".page-heading__title", geography.short_name);

    new LinkField(".page-options__link-download-pdf", pdfUrl);

    var url = window.location.toString();

    // social buttons
    $('.page-options__link-share-facebook').on('click', function(e) {
      e.preventDefault();

      window.open(`https://www.facebook.com/dialog/share?app_id=670170087018628&href=${encodeURIComponent(url)}`,
                  "share", "width=600, height=400, scrollbars=no");
      ga('send', 'social', 'facebook', 'share', url);
    });

    $('.page-options__link-share-twitter').on('click', function(e) {
      e.preventDefault();
      var tweet = $(this).data('tweet') || '';

      window.open("https://twitter.com/intent/tweet?" +
                  "text=" + encodeURIComponent(tweet) +
                  "&url=" + encodeURIComponent(url),
                  "share", "width=364, height=250, scrollbars=no");
      ga('send', 'social', 'twitter', 'share', url);
    });

  }
}
