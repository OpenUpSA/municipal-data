import { focusBlock } from '../utils.js';

export default class HelpPage {
  constructor() {
    if (location.hash) {
      focusBlock(location.hash.substr(1));
    }
  }
}

const videos = {
  "Introduction to Municapal Finances": {
    "description": "short description", "files": [
      { "language": "English", "size": ["100"] },
      { "language": "Afrikaans", "size": ["110"] },
    ]
  }
};
const infoVideo = $("#training .sub-section");
const title = ".informational-video_title";
const desc = ".informational-video_info p"
const drCurrentLang = ".language-dropdown .dropdown__current-select";
const drCurrentSize = ".size-dropdown .dropdown__current-select:last";
const drLangList = ".language-dropdown .dropdown-list";
const drSizeList = ".size-dropdown .dropdown-list";
let drItem = $("<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0'></a>");

//$(".informational-video_block:first").hide();
$(drLangList).empty();
$(drSizeList).empty();

$.each(videos, function (key, value) {
  //console.log(this);
  var videoBlock = $(".informational-video_block:first").clone();
  videoBlock.find(title).text(key);
  videoBlock.find(desc).text(this.description);
  //videoBlock.find(drCurrentLang).text("");
  //videoBlock.find(drCurrentSize).text("");

  $.each(this.files, function (index, item) {
    console.log(item);
    drItem.text(item.language);
    videoBlock.find(drLangList).append(drItem);

    $.each(item.size, function (index, size) {
      drItem.text(size);
      videoBlock.find(drSizeList).append(drItem);
    });
  });
  videoBlock.appendTo(infoVideo);
});

/*var videoBlock = $(".informational-video_block:first").clone();
videoBlock.find('.informational-video_title').text('Video two');
videoBlock.appendTo(infoVideo);*/
