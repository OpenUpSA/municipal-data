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
  },
};
const infoVideo = $("#training .sub-section");
const title = ".informational-video_title";
const desc = ".informational-video_info p"
const drCurrentLang = ".language-dropdown .dropdown__current-select";
const drCurrentSize = ".size-dropdown .dropdown__current-select";
const dropdownLangItems = ".language-dropdown .dropdown-list";
const dropdownSizeItems = ".size-dropdown .dropdown-list";
let dropdownItem = $("<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0'></a>");

//$(".informational-video_block:first").hide();
//$(dropdownSizeItems).empty();
//$(dropdownSizeItems).empty();

$.each(videos, function (key, value) {
  var videoBlock = $(".informational-video_block:first").clone();
  videoBlock.find(title).text(key);
  videoBlock.find(desc).text(this.description);
  //videoBlock.find(drCurrentLang).text("");
  //videoBlock.find(drCurrentSize).text("");

  $.each(this.files, function (index, file) {
    console.log(file);
    dropdownItem.text(file.language);
    videoBlock.find(dropdownLangItems).append(dropdownItem);

    /*$.each(file.size, function (index, size) {
      dropdownItem.text(size);
      videoBlock.find(dropdownSizeItems).append(dropdownItem);
    });*/
  });
  videoBlock.appendTo(infoVideo);
});
