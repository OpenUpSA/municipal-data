import { focusBlock } from '../utils.js';

export default class HelpPage {
  constructor() {
    if (location.hash) {
      focusBlock(location.hash.substr(1));
    }
  }
}

const videos = {
  'Introduction to Municapal Finance': {
    description: '',
    embed: 'HeQiX_e8ubg',
    options: [
      { language: 'English', files: { 66.9: 'Municipal_Money%3A_Intro_to_Municipal_Finance_English.mp4', 27.7: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BEnglish.mp4' } },
      { language: 'isiXhosa', files: { 73.2: 'Municipal_Money%3A_Intro_to_Municipal_Finance_isiXhosa.mp4', 30.4: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BisiXhosa.mp4' } },
      { language: 'Afrikaans', files: { 82.5: 'Municipal_Money%3A_Intro_to_Municipal_Finance_Afrikaans.mp4', 27.8: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BAfrikaans.mp4' } },
      { language: 'Sotho', files: { 76.9: 'Municipal_Money%3A_Intro_to_Municipal_Finance_Sotho.mp4', 27.7: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BSotho.mp4' } },
      { language: 'Zulu', files: { 87.2: 'Municipal_Money%3A_Intro_to_Municipal_Finance_Zulu.mp4', 31.3: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BZulu.mp4' } },
    ],
  },
  'Irregular, Fruitless and Wasteful Expenditure': {
    description: '',
    embed: 'WVZBVJTh0u0',
    options: [
      { language: 'English', files: { 22.7: 'Municipal_Money%3A_Irregular%2C_Fruitless_and_Wasteful_Expenditure.mp4', '9.0': 'compressed/Municipal%2BMoney_%2BIrregular%2C%2BFruitless%2Band%2BWasteful%2BExpenditure.mp4' } },
    ],
  },
  Liquidity: {
    description: '',
    embed: '6WUDTN7kBZI',
    options: [
      { language: 'English', files: { 13.6: 'Municipal_Money%3A_Liquidity.mp4', 10.7: 'compressed/Municipal%2BMoney_%2BLiquidity.mp4' } },
    ],
  },
  'Sources of Income': {
    description: '',
    embed: 'zb2Wph6Mbpo',
    options: [
      { language: 'English', files: { '6.0': 'Municipal_Money%3A_Sources_of_Income.mp4' } },
    ],
  },
  'Spending of the Capital Budget': {
    description: '',
    embed: 'L7rfUkK5PJI',
    options: [
      { language: 'English', files: { 12.5: 'Municipal_Money%3A_Spending_of_the_Capital_Budget.mp4', 4.5: 'compressed/Municipal%2BMoney_%2BSpending%2Bof%2Bthe%2BCapital%2BBudget.mp4' } },
    ],
  },
  'Spending of the Operating Budget': {
    description: '',
    embed: 'r8_W4Yn0Oz8',
    options: [
      { language: 'English', files: { 13.8: 'Municipal_Money%3A_Spending_of_the_Operating_Budget.mp4', 5.1: 'compressed/Municipal%2BMoney_%2BSpending%2Bof%2Bthe%2BOperating%2BBudget.mp4' } },
    ],
  },
  'Spending on Repairs & Maintenance': {
    description: '',
    embed: 'f2CdUnsEBXA',
    options: [
      { language: 'English', files: { 11.8: 'Municipal_Money%3A_Spending_on_Repairs_%26_Maintenance.mp4', 4.9: 'compressed/Municipal%2BMoney_%2BSpending%2Bon%2BRepairs%2B_%2BMaintenance.mp4' } },
    ],
  },
  'Cash Balances and Cash Coverage': {
    description: '',
    embed: '-sGcopgP4u0',
    options: [
      { language: 'English', files: { 22.5: 'Municipal_Money%3A_Cash_Balances_and_Cash_Coverage.mp4', '7.0': 'compressed/Municipal%2BMoney_%2BCash%2BBalances%2Band%2BCash%2BCoverage.mp4' } },
    ],
  },
  "Debtors' Collections Ratio": {
    description: '',
    embed: 'A15Fvwcx_OY',
    options: [
      { language: 'English', files: { 11.8: "Municipal_Money%3A_Debtors'_Collections_Ratio.mp4", 4.5: 'compressed/Municipal%2BMoney%2BDebtors_%2BCollections%2BRatio.mp4' } },
    ],
  },
};

const videoStorage = 'https://munimoney-media.s3.eu-west-1.amazonaws.com/info-videos/';
const infoVideo = $('#training .sub-section');
const title = '.informational-video_title';
const desc = '.informational-video_info p';
const currentLang = '.language-dropdown .dropdown__current-select';
const currentSize = '.size-dropdown .dropdown__current-select';
const toggleLang = '.language-dropdown .dropdown-toggle';
const dropdownLangItems = '.language-dropdown .dropdown-list';
const dropdownSizeItems = '.size-dropdown .dropdown-list';
const dropdownItem = "<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0'>";
const downloadBtn = '.informational-video_download-button';

$(dropdownLangItems).empty();
$(dropdownSizeItems).empty();

$.each(videos, function (name, value) {
  var videoBlock = $('.informational-video_block:first').clone();
  const defaultVideo = value.options[0];
  const fileSize = Object.keys(defaultVideo.files)[0];
  let appendLang = '';

  videoBlock.find(title).text(name);
  videoBlock.find(desc).text(this.description);
  videoBlock.find(currentLang).text(value.options[0].language);
  videoBlock.find(currentSize).text(`${fileSize} MB`);
  videoBlock.find(downloadBtn).attr('href', videoStorage + value.options[0].files[fileSize]);

  // Disable language dropdown with only one option
  if (value.options.length <= 1 && videoBlock.find(toggleLang).length > 0) {
    videoBlock.find(toggleLang)[0].style.cursor = 'default';
    videoBlock.find(toggleLang)[0].style.pointerEvents = 'none';
    videoBlock.find(toggleLang)[0].style.opacity = '0.7';
  }

  const videoEmbed = `<iframe frameborder='0' src='https://www.youtube.com/embed/${value.embed}'></iframe>`;
  videoBlock.find('.informational-video_video-wrapper').html(videoEmbed);

  $.each(this.options, (index, video) => {
    appendLang += `<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0' value='${name}'>${video.language}</a>`;
    let appendSize = '';
    if (video.language == videoBlock.find(currentLang).text()) {
      Object.keys(video.files).forEach((size) => {
        appendSize += `<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0' value='${video.files[size]}'>${size} MB</a>`;
      });
    }
    videoBlock.find(dropdownSizeItems).append(appendSize);
  });

  videoBlock.find(dropdownLangItems).append(appendLang);
  videoBlock.appendTo(infoVideo);
});

$('.informational-video_block:first').hide();

function changeLanguage(e) {
  $(e.target.parentElement.parentElement.children[0].children[1]).text(this.text);
  $('.dropdown-list').removeClass('w--open');
  $('.dropdown-toggle').removeClass('w--open');
  $('.dropdown-toggle').attr('aria-expanded', 'false');
  $('.dropdown').attr('style', '');

  const name = this.getAttribute('value');

  $.each(videos[name].options, (index, video) => {
    let appendSize = '';
    let defaultSize; let
      defaultVideo;

    if (video.language == this.text) {
      defaultSize = Object.keys(video.files)[0];
      defaultVideo = video.files[defaultSize];
      Object.keys(video.files).forEach((size) => {
        appendSize += `<a href='#' data-option='none' class='dropdown-link dropdown-link--current w-dropdown-link' tabindex='0' value='${video.files[size]}'>${size} MB</a>`;
      });
    }

    if (typeof defaultSize !== 'undefined') {
      // Set current selection
      e.target.parentElement.parentElement.parentElement.parentElement.children[1].children[1].children[0].children[1].innerHTML = `${defaultSize} MB`;
      // Set size dropdown list
      e.target.parentElement.parentElement.parentElement.parentElement.children[1].children[1].children[1].innerHTML = appendSize;
      // Set download button href
      e.target.parentElement.parentElement.parentElement.parentElement.children[2].href = `${videoStorage}${defaultVideo}`;
    }
  });
}
function changeSize(e) {
  $(e.target.offsetParent.offsetParent.children[0].children[1]).text(this.text);
  $('.dropdown-list').removeClass('w--open');
  $('.dropdown-toggle').removeClass('w--open');
  $('.dropdown-toggle').attr('aria-expanded', 'false');
  $('.dropdown').attr('style', '');
  // Set download button href
  e.target.parentElement.parentElement.parentElement.parentElement.children[2].href = `${videoStorage}${this.getAttribute('value')}`;
}
function dropdownlist(e) {
  setTimeout(() => {
    if (e.currentTarget.children[0].attributes['aria-expanded'].value == 'true') {
      e.currentTarget.children[0].children[1].style.opacity = 0;
    }
  }, 0);
}
function showcurrent(e) {
  $(currentLang).attr('style', '');
  $(currentSize).attr('style', '');
}

$('body').on('click', showcurrent);
$('.language-dropdown').on('click', dropdownlist);
$('.size-dropdown').on('click', dropdownlist);
$('.language-dropdown .dropdown-link').on('click', changeLanguage);
$('.size-dropdown .dropdown-link').on('click', changeSize);
