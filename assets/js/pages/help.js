import { focusBlock } from '../utils.js';

export default class HelpPage {
  constructor() {
    if (location.hash) {
      focusBlock(location.hash.substr(1));
    }
  }
}

const videos = {
  "Introduction to Municapal Finance": {
    description: "",
    embed: "HeQiX_e8ubg",
    options: [
      { language: "English", files: { "61.3": "Municipal+Money%3A+Intro+to+Municipal+Finance+English.webm", "1.0": "asdf.webm" } },
      { language: "Afrikaans", files: { "94.1": "Municipal+Money%3A+Intro+to+Municipal+Finance+Afrikaans.mkv", } },
    ],
  },
  "Irregular, Fruitless and Wasteful Expenditure": {
    description: "",
    embed: "WVZBVJTh0u0",
    options: [
      { language: "English", files: { "25.5": "Municipal+Money%3A+Irregular%2C+Fruitless+and+Wasteful+Expenditure.mkv", } },
    ],
  },
  "Liquidity": {
    description: "",
    embed: "6WUDTN7kBZI",
    options: [
      { language: "English", files: { "14.9": "Municipal+Money%3A+Liquidity.mkv", } },
    ],
  },
  "Sources of Income": {
    description: "",
    embed: "zb2Wph6Mbpo",
    options: [
      { language: "English", files: { "4.9": "Municipal+Money%3A+Sources+of+Income.webm", } },
    ],
  },
  "Spending of the Capital Budget": {
    description: "",
    embed: "L7rfUkK5PJI",
    options: [
      { language: "English", files: { "9.2": "Municipal+Money%3A+Spending+of+the+Capital+Budget.webm", } },
    ],
  },
  "Spending of the Operating Budget": {
    description: "",
    embed: "r8_W4Yn0Oz8",
    options: [
      { language: "English", files: { "10.3": "Municipal+Money%3A+Spending+of+the+Operating+Budget.webm", } },
    ],
  },
  "Spending on Repairs & Maintenance": {
    description: "",
    embed: "f2CdUnsEBXA",
    options: [
      { language: "English", files: { "10.2": "Municipal+Money%3A+Spending+on+Repairs+%26+Maintenance.webm", } },
    ],
  },
  "Cash Balances and Cash Coverage": {
    description: "",
    embed: "-sGcopgP4u0",
    options: [
      { language: "English", files: { "16.3": "Municipal+Money%3A+Cash+Balances+and+Cash+Coverage.webm", } },
    ],
  },
  "Debtors' Collections Ratio": {
    description: "",
    embed: "A15Fvwcx_OY",
    options: [
      { language: "English", files: { "13.1": "Municipal+Money+Debtors'+Collections+Ratio.mkv", } },
    ],
  },
};

const videoStorage = "https://munimoney-media.s3.eu-west-1.amazonaws.com/info-videos/";
const infoVideo = $('#training .sub-section');
const title = ".informational-video_title";
const desc = ".informational-video_info p";
const currentLang = ".language-dropdown .dropdown__current-select";
const currentSize = ".size-dropdown .dropdown__current-select";
const toggleLang = ".language-dropdown .dropdown-toggle";
const dropdownLangItems = ".language-dropdown .dropdown-list";
const dropdownSizeItems = ".size-dropdown .dropdown-list";
const dropdownItem = "<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0'>";
const downloadBtn = ".informational-video_download-button";

$(dropdownLangItems).empty();
$(dropdownSizeItems).empty();

$.each(videos, function (name, value) {
  var videoBlock = $(".informational-video_block:first").clone();
  let defaultVideo = value.options[0];
  let fileSize = Object.keys(defaultVideo.files)[0];
  let appendLang = "";

  videoBlock.find(title).text(name);
  videoBlock.find(desc).text(this.description);
  videoBlock.find(currentLang).text(value.options[0].language);
  videoBlock.find(currentSize).text(fileSize + " MB");
  videoBlock.find(downloadBtn).attr("href", videoStorage + value.options[0].files[fileSize]);

  // Disable language dropdown with only one option
  if (value.options.length <= 1 && videoBlock.find(toggleLang).length > 0) {
    videoBlock.find(toggleLang)[0].style.cursor = 'default';
    videoBlock.find(toggleLang)[0].style.pointerEvents = 'none';
    videoBlock.find(toggleLang)[0].style.opacity = '0.7';
  }

  let videoEmbed = `<iframe frameborder='0' src='https://www.youtube.com/embed/${value.embed}'></iframe>`
  videoBlock.find(".informational-video_video-wrapper").html(videoEmbed);

  $.each(this.options, (index, video) => {
    appendLang += `<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0' value='${name}'>${video.language}</a>`;
    let appendSize = "";
    if (video.language == videoBlock.find(currentLang).text()) {
      Object.keys(video.files).forEach(size => {
        appendSize += `<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0' value='${video.files[size]}'>${size} MB</a>`
      });
    }
    videoBlock.find(dropdownSizeItems).append(appendSize);
  });

  videoBlock.find(dropdownLangItems).append(appendLang);
  videoBlock.appendTo(infoVideo);
});

$(".informational-video_block:first").hide();

function changeLanguage(e) {
  $(e.target.parentElement.parentElement.children[0].children[1]).text(this.text);
  $(".dropdown-list").removeClass("w--open");
  $(".dropdown-toggle").removeClass("w--open");
  $(".dropdown-toggle").attr("aria-expanded", "false");
  $(".dropdown").attr("style", "");

  let name = this.getAttribute("value");

  $.each(videos[name].options, (index, video) => {
    let appendSize = "";
    let defaultSize, defaultVideo;

    if (video.language == this.text) {
      defaultSize = Object.keys(video.files)[0];
      defaultVideo = video.files[defaultSize];
      Object.keys(video.files).forEach(size => {
        appendSize += `<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0' value='${video.files[size]}'>${size} MB</a>`
      });
    }

    // Set current selection
    if (typeof defaultSize !== "undefined") {
      e.target.parentElement.parentElement.parentElement.parentElement.children[1].children[1].children[0].children[1].innerHTML = `${defaultSize} MB`;
    }
    // Set dropdown list
    e.target.parentElement.parentElement.parentElement.parentElement.children[1].children[1].children[1].innerHTML = appendSize;
    // Set download button href
    e.target.parentElement.parentElement.parentElement.parentElement.children[2].href = defaultVideo;
  });
}
function changeSize(e) {
  $(e.target.offsetParent.offsetParent.children[0].children[1]).text(this.text);
  $(".dropdown-list").removeClass("w--open");
  // Set download button href
  e.target.parentElement.parentElement.parentElement.parentElement.children[2].href = this.getAttribute("value");
}
function dropdownlist(e) {
  setTimeout(function () {
    if (e.currentTarget.children[0].attributes['aria-expanded'].value == "true") {
      e.currentTarget.children[0].children[1].style.opacity = 0;
    }
  }, 0);
}
function showcurrent(e) {
  $(currentLang).attr("style", "");
}

$("body").on("click", showcurrent);
$(".language-dropdown").on("click", dropdownlist);
$(".language-dropdown .dropdown-link").on("click", changeLanguage);
$(".size-dropdown .dropdown-link").on("click", changeSize);
