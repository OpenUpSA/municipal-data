import { focusBlock } from '../utils.js';
import ReactDOM from 'react-dom'
import * as React from 'react';
import Button from '@mui/material/Button';

export default class HelpPage {
  constructor() {
    if (location.hash) {
      focusBlock(location.hash.substr(1));
    }

    const ReactBtn = () => (
      <Button variant="contained" color="primary">
        Hello World
      </Button>
    );
    ReactDOM.render(<ReactBtn />, document.getElementById("react-test"));

  }
}



const videos = {
  'Introduction to Municapal Finances': {
    description: 'short description',
    files: [
      { language: 'English', size: ['100'] },
      { language: 'Afrikaans', size: ['110'] },
    ],
  },
};

const infoVideo = $('#training .sub-section');
const title = '.informational-video_title';
const desc = '.informational-video_info p';
const drCurrentLang = '.language-dropdown .dropdown__current-select';
const drCurrentSize = '.size-dropdown .dropdown__current-select';
const dropdownLangItems = '.language-dropdown .dropdown-list';
const dropdownSizeItems = '.size-dropdown .dropdown-list';
const dropdownItem = $("<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0'></a>");
const dropdownItem2 = "<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0'>";

// $(".informational-video_block:first").hide();
$(dropdownLangItems).empty();
$(dropdownSizeItems).empty();

$.each(videos, function (key, value) {
  var videoBlock = $('.informational-video_block:first').clone();
  videoBlock.find(title).text(key);
  videoBlock.find(desc).text(this.description);
  // videoBlock.find(drCurrentLang).text("");
  // videoBlock.find(drCurrentSize).text("");
  let appendLang = "";
  let appendSize = "";

  $.each(this.files, (index, file) => {
    appendLang += dropdownItem2 + file.language + "</a>";
    $.each(file.size, function (index, size) {
      appendSize += dropdownItem2 + size + "</a>";
    });
    videoBlock.find(dropdownSizeItems).append(appendSize);
  });

  videoBlock.find(dropdownLangItems).append(appendLang);
  videoBlock.appendTo(infoVideo);
});
