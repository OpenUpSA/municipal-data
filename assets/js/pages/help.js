import { focusBlock } from '../utils.js';
import Dropdown from '../components/grouped_dropdowns.js';

export default class HelpPage {
  constructor() {
    if (location.hash) {
      focusBlock(location.hash.substr(1));
    }
  }
}

const videoStorage = 'https://munimoney-media.s3.eu-west-1.amazonaws.com/info-videos/';
const infoVideo = $('#training .sub-section');
const title = '.informational-video_title';
const desc = '.informational-video_info p';
const toggleLang = '.language-dropdown .dropdown-toggle';
const downloadBtn = '.informational-video_download-button';
const currentLang = '.language-dropdown .dropdown__current-select';
const currentSize = '.size-dropdown .dropdown__current-select';

const videos = {
  'Introduction to Municapal Finance': {
    description: '',
    embed: 'HeQiX_e8ubg',
    options: [
      ['English', { 66.9: 'Municipal_Money%3A_Intro_to_Municipal_Finance_English.mp4', 27.7: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BEnglish.mp4' }],
      ['isiXhosa', { 73.2: 'Municipal_Money%3A_Intro_to_Municipal_Finance_isiXhosa.mp4', 30.4: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BisiXhosa.mp4' }],
      ['Afrikaans', { 82.5: 'Municipal_Money%3A_Intro_to_Municipal_Finance_Afrikaans.mp4', 27.8: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BAfrikaans.mp4' }],
      ['Sotho', { 76.9: 'Municipal_Money%3A_Intro_to_Municipal_Finance_Sotho.mp4', 27.7: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BSotho.mp4' }],
      ['Zulu', { 87.2: 'Municipal_Money%3A_Intro_to_Municipal_Finance_Zulu.mp4', 31.3: 'compressed/Municipal%2BMoney_%2BIntro%2Bto%2BMunicipal%2BFinance%2BZulu.mp4' }],
    ],
  },
  'Irregular, Fruitless and Wasteful Expenditure': {
    description: '',
    embed: 'WVZBVJTh0u0',
    options: [
      ['English', { 22.7: 'Municipal_Money%3A_Irregular%2C_Fruitless_and_Wasteful_Expenditure.mp4', '9.0': 'compressed/Municipal%2BMoney_%2BIrregular%2C%2BFruitless%2Band%2BWasteful%2BExpenditure.mp4' }],
    ],
  },
  Liquidity: {
    description: '',
    embed: '6WUDTN7kBZI',
    options: [
      ['English', { 13.6: 'Municipal_Money%3A_Liquidity.mp4', 10.7: 'compressed/Municipal%2BMoney_%2BLiquidity.mp4' }],
    ],
  },
  'Sources of Income': {
    description: '',
    embed: 'zb2Wph6Mbpo',
    options: [
      ['English', { '6.0': 'Municipal_Money%3A_Sources_of_Income.mp4' }],
    ],
  },
  'Spending of the Capital Budget': {
    description: '',
    embed: 'L7rfUkK5PJI',
    options: [
      ['English', { 12.5: 'Municipal_Money%3A_Spending_of_the_Capital_Budget.mp4', 4.5: 'compressed/Municipal%2BMoney_%2BSpending%2Bof%2Bthe%2BCapital%2BBudget.mp4' }],
    ],
  },
  'Spending of the Operating Budget': {
    description: '',
    embed: 'r8_W4Yn0Oz8',
    options: [
      ['English', { 13.8: 'Municipal_Money%3A_Spending_of_the_Operating_Budget.mp4', 5.1: 'compressed/Municipal%2BMoney_%2BSpending%2Bof%2Bthe%2BOperating%2BBudget.mp4' }],
    ],
  },
  'Spending on Repairs & Maintenance': {
    description: '',
    embed: 'f2CdUnsEBXA',
    options: [
      ['English', { 11.8: 'Municipal_Money%3A_Spending_on_Repairs_%26_Maintenance.mp4', 4.9: 'compressed/Municipal%2BMoney_%2BSpending%2Bon%2BRepairs%2B_%2BMaintenance.mp4' }],
    ],
  },
  'Cash Balances and Cash Coverage': {
    description: '',
    embed: '-sGcopgP4u0',
    options: [
      ['English', { 22.5: 'Municipal_Money%3A_Cash_Balances_and_Cash_Coverage.mp4', '7.0': 'compressed/Municipal%2BMoney_%2BCash%2BBalances%2Band%2BCash%2BCoverage.mp4' }],
    ],
  },
  "Debtors' Collections Ratio": {
    description: '',
    embed: 'A15Fvwcx_OY',
    options: [
      ['English', { 11.8: "Municipal_Money%3A_Debtors'_Collections_Ratio.mp4", 4.5: 'compressed/Municipal%2BMoney%2BDebtors_%2BCollections%2BRatio.mp4' }],
    ],
  },
};

$.each(videos, function (name, value) {
  var videoBlock = $('.informational-video_block:first').clone();
  videoBlock.find(title).text(name);
  videoBlock.find(desc).text(this.description);

  const initialLang = value.options[0][0];
  const initialSize = Object.keys(value.options[0][1])[0];
  videoBlock.find(downloadBtn).attr('href', videoStorage + value.options[0][1][initialSize]);

  // Set size dropdown on initial load and select events
  this.dropdown = new Dropdown(videoBlock.find('.language-dropdown'), value.options, initialLang, initialSize, videoBlock.find('.size-dropdown'));
  this.dropdown.$element.on('option-select', (e) => {
    videoBlock.find(downloadBtn).attr('href', `${videoStorage}${e.detail}`);
  });
  this.dropdown.$linkedElement.on('option-select', (e) => {
    videoBlock.find(downloadBtn).attr('href', `${videoStorage}${e.detail}`);
  });

  // Disable language dropdown with only one option
  if (value.options.length <= 1 && videoBlock.find(toggleLang).length > 0) {
    videoBlock.find(toggleLang)[0].style.cursor = 'default';
    videoBlock.find(toggleLang)[0].style.pointerEvents = 'none';
    videoBlock.find(toggleLang)[0].style.opacity = '0.7';
  }

  const videoEmbed = `<iframe frameborder='0' src='https://www.youtube.com/embed/${value.embed}'></iframe>`;
  videoBlock.find('.informational-video_video-wrapper').html(videoEmbed);
  videoBlock.appendTo(infoVideo);
});

$('.informational-video_block:first').hide();


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

