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
  "Introduction to Municapal Finance": {
    description: "",
    options: [
      { language: "English", files: { "61.3": "Municipal+Money%3A+Intro+to+Municipal+Finance+English.webm", } },
      { language: "Afrikaans", files: { "94.1": "Municipal+Money%3A+Intro+to+Municipal+Finance+Afrikaans.mkv", } },
    ],
  },
  "Irregular, Fruitless and Wasteful Expenditure": {
    description: "",
    options: [
      { language: "English", files: { "25.5": "Municipal+Money%3A+Irregular%2C+Fruitless+and+Wasteful+Expenditure.mkv", } },
    ],
  },
  "Liquidity": {
    description: "",
    options: [
      { language: "English", files: { "14.9": "Municipal+Money%3A+Liquidity.mkv", } },
    ],
  },
  "Sources of Income": {
    description: "",
    options: [
      { language: "English", files: { "4.9": "Municipal+Money%3A+Sources+of+Income.webm", } },
    ],
  },
  "Spending of the Capital Budget": {
    description: "",
    options: [
      { language: "English", files: { "9.2": "Municipal+Money%3A+Spending+of+the+Capital+Budget.webm", } },
    ],
  },
  "Spending of the Operating Budget": {
    description: "",
    options: [
      { language: "English", files: { "10.3": "Municipal+Money%3A+Spending+of+the+Operating+Budget.webm", } },
    ],
  },
  "Spending on Repairs & Maintenance": {
    description: "",
    options: [
      { language: "English", files: { "10.2": "Municipal+Money%3A+Spending+on+Repairs+%26+Maintenance.webm", } },
    ],
  },
};

const videoStorage = "https://munimoney-media.s3.eu-west-1.amazonaws.com/info-videos/";
const infoVideo = $('#training .sub-section');
const title = ".informational-video_title";
const desc = ".informational-video_info p";
const drCurrentLang = ".language-dropdown .dropdown__current-select";
const drCurrentSize = ".size-dropdown .dropdown__current-select";
const dropdownLangItems = ".language-dropdown .dropdown-list";
const dropdownSizeItems = ".size-dropdown .dropdown-list";
const dropdownItem = "<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0'>";

//$(".informational-video_block:first").hide();
$(dropdownLangItems).empty();
$(dropdownSizeItems).empty();

$.each(videos, function (key, value) {
  var videoBlock = $(".informational-video_block:first").clone();
  videoBlock.find(title).text(key);
  videoBlock.find(desc).text(this.description);
  videoBlock.find(drCurrentLang).text(value.options[0].language);
  let fileSize = Object.keys(value.options[0].files)[0];
  videoBlock.find(drCurrentSize).text(fileSize);
  let appendLang = "";


  $.each(this.options, (index, file) => {
    appendLang += dropdownItem + file.language + "</a>";
    let appendSize = "";
    $.each(file.size, function (index, size) {
      appendSize += dropdownItem + size + "</a>";
    });
    videoBlock.find(dropdownSizeItems).append(appendSize);
  });

  videoBlock.find(dropdownLangItems).append(appendLang);
  videoBlock.appendTo(infoVideo);
});

function changeLanguage() {
  console.log(this);
}
function changeSize() {
  console.log(this);
}
function downloadVideo() {
  console.log(this);
}
$(".language-dropdown .dropdown-link").on("click", changeLanguage);
$(".size-dropdown .dropdown-link").on("click", changeSize);
$(".informational-video_download-button").on("click", downloadVideo);
