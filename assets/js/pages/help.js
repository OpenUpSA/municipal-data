import { focusBlock } from '../utils.js';
import Dropdown from '../components/dropdown.js';

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
const toggleLang = '.is-language-dropdown .dropdown-toggle';
const downloadBtn = '.informational-video_download-button';

const videos = {
  'Introduction to Municipal Finance': {
    description: 'An overview of where Municipal Money fits into the process of participating in local government.',
    embed: 'HeQiX_e8ubg',
    languages: [
      ['English', 'eng'],
      ['isiXhosa', 'xhosa'],
      ['Afrikaans', 'afr'],
      ['Sotho', 'sotho'],
      ['Zulu', 'zulu'],
    ],
    files: {
      eng: [['66.9 MB (Full size)', 'Municipal_Money%3A_Intro_to_Municipal_Finance_English.mp4'], ['14.9 MB (Small size)', 'compressed/Municipal_Money%3A_Intro_to_Municipal_Finance_English.mp4']],
      xhosa: [['73.2 MB (Full size)', 'Municipal_Money%3A_Intro_to_Municipal_Finance_isiXhosa.mp4'], ['30.4 MB (Small size)', 'compressed/Municipal_Money%3A_Intro_to_Municipal_Finance_isiXhosa.mp4']],
      afr: [['82.5 MB (Full size)', 'Municipal_Money%3A_Intro_to_Municipal_Finance_Afrikaans.mp4'], ['27.8 MB (Small size)', 'compressed/Municipal_Money%3A_Intro_to_Municipal_Finance_Afrikaans.mp4']],
      sotho: [['76.9 MB (Full size)', 'Municipal_Money%3A_Intro_to_Municipal_Finance_Sotho.mp4'], ['27.7 MB (Small size)', 'compressed/Municipal_Money%3A_Intro_to_Municipal_Finance_Sotho.mp4']],
      zulu: [['87.2 MB (Full size)', 'Municipal_Money%3A_Intro_to_Municipal_Finance_Zulu.mp4'], ['14.9 MB (Small size)', 'compressed/Municipal_Money%3A_Intro_to_Municipal_Finance_Zulu.mp4']],
    },
    sectionMarkers: ['intro'],
  },
  'Unauthorized, Irregular, Fruitless and Wasteful Expenditure': {
    description: 'Expediture that was not budgeted for.',
    embed: 'WVZBVJTh0u0',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['22.7 MB (Full size)', 'Municipal_Money%3A_Irregular%2C_Fruitless_and_Wasteful_Expenditure.mp4'], ['9.0 MB (Small size)', 'compressed/Municipal_Money%3A_Irregular%2C_Fruitless_and_Wasteful_Expenditure.mp4']],
    },
    sectionMarkers: ['wasteful-expenditure'],
  },
  Liquidity: {
    description: 'Ability to meet liabilities.',
    embed: '6WUDTN7kBZI',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['13.6 MB (Full size)', 'Municipal_Money%3A_Liquidity.mp4'], ['10.7 MB (Small size)', 'compressed/Municipal_Money%3A_Liquidity.mp4']],
    },
    sectionMarkers: ['liquidity-ratio', 'current-ratio'],
  },
  'Sources of Income': {
    description: 'Where a municipality draws revenue from.',
    embed: 'zb2Wph6Mbpo',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['6.0 MB (Small size)', 'Municipal_Money%3A_Sources_of_Income.mp4']],
    },
    sectionMarkers: ['income'],
  },
  'Spending of the Capital Budget': {
    description: 'The Capital Budget is allocated to spending on infrastructure projects.',
    embed: 'L7rfUkK5PJI',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['12.5 MB (Full size)', 'Municipal_Money%3A_Spending_of_the_Capital_Budget.mp4'], ['4.5 MB (Small size)', 'compressed/Municipal_Money%3A_Spending_of_the_Capital_Budget.mp4']],
    },
    sectionMarkers: ['capital-budget'],
  },
  'Spending of the Operating Budget': {
    description: 'The Operating Budget is for day to day spending such as salaries, water and electricity.',
    embed: 'r8_W4Yn0Oz8',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['13.8 MB (Full size)', 'Municipal_Money%3A_Spending_of_the_Operating_Budget.mp4'], ['5.1 MB (Small size)', 'compressed/Municipal_Money%3A_Spending_of_the_Operating_Budget.mp4']],
    },
    sectionMarkers: ['operating-budget'],
  },
  'Spending on Repairs & Maintenance': {
    description: 'Maintenance and renewal of infrastructure',
    embed: 'f2CdUnsEBXA',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['11.8 MB (Full size)', 'Municipal_Money%3A_Spending_on_Repairs_%26_Maintenance.mp4'], ['4.9 MB (Small size)', 'compressed/Municipal_Money%3A_Spending_on_Repairs_Maintenance.mp4']],
    },
    sectionMarkers: ['repairs-maintenance'],
  },
  'Cash Balances and Cash Coverage': {
    description: 'Cash balance is money left after paying expenses. Cash coverage is the ability to cover recurring costs.',
    embed: '-sGcopgP4u0',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['22.5 MB (Full size)', 'Municipal_Money%3A_Cash_Balances_and_Cash_Coverage.mp4'], ['7.0 MB (Small size)', 'compressed/Municipal_Money%3A_Cash_Balances_and_Cash_Coverage.mp4']],
    },
    sectionMarkers: ['cash-balance', 'cash-coverage'],
  },
  "Debtors' Collections Ratio": {
    description: 'How well a municipality is meeting it\'s revenue targets',
    embed: 'A15Fvwcx_OY',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['11.8 MB (Full size)', "Municipal_Money%3A_Debtors'_Collections_Ratio.mp4"], ['4.5 MB (Small size)', 'compressed/Municipal_Money%3A_Debtors_Collections_Ratio.mp4']],
    },
    sectionMarkers: ['collection-rate'],
  },
  'Conditional Grants': {
    description: 'A municipalities revenue source originating from National Government that has rules on where it should be spent',
    embed: 'bXL3p5khtio',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['57.4 MB (Full size)', 'Municipal_Money%3A_Conditional_Grants.mp4'], ['8.7 MB (Small size)', 'compressed/Municipal_Money%3A_Conditional_Grants.mp4']],
    },
    sectionMarkers: ['grants'],
  },
  'Household Bills': {
    description: 'Income sources originating from residents',
    embed: 'GwvMI2GVwCg',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['129.6 MB (Full size)', 'Municipal_Money%3A_Household_Bills.mp4'], ['13.9 MB (Small size)', 'compressed/Municipal_Money%3A_Household_Bills.mp4']],
    },
    sectionMarkers: ['household'],
  },
  'Capital Projects': {
    description: 'Short overview of municipal budgeting with regard to capital projects.',
    embed: 'i7KdL1b9tPk',
    languages: [
      ['English', 'eng'],
    ],
    files: {
      eng: [['12.2 MB (Full size)', 'Municipal_Money%3A_Capital_Projects.mp4'], ['3.0 MB (Small size)', 'compressed/Municipal_Money%3A_Capital_Projects.mp4']],
    },
    sectionMarkers: ['municipal-budget'],
  },
};

$.each(videos, function (name, value) {
  var videoBlock = $('.informational-video_block:first').clone();
  videoBlock.find(title).text(name);
  videoBlock.find(desc).text(this.description);

  const initialLang = value.languages[0];
  const initialFile = value.files[initialLang[1]][0];
  videoBlock.find(downloadBtn).attr('href', videoStorage + initialFile[1]);

  this.dropdownLanguage = new Dropdown(videoBlock.find('.download-bar_select:first'), value.languages, initialLang[0]);
  this.dropdownSize = new Dropdown(videoBlock.find('.download-bar_select:eq( 1 )'), value.files[initialLang[1]], initialFile[0]);

  this.dropdownLanguage.$element.on('option-select', (e) => {
    const defaultFile = value.files[e.detail][0];
    this.dropdownSize = new Dropdown(videoBlock.find('.download-bar_select:eq( 1 )'), value.files[e.detail], defaultFile[0]);
    videoBlock.find(downloadBtn).attr('href', `${videoStorage}${defaultFile[1]}`);
  });
  this.dropdownSize.$element.on('option-select', (e) => {
    videoBlock.find(downloadBtn).attr('href', `${videoStorage}${e.detail}`);
  });

  // Disable language dropdown with only one option
  if (value.languages.length <= 1) {
    $(videoBlock.find(toggleLang)).addClass('dropdown-toggle--disabled');
  }

  const videoEmbed = `<iframe width='100%' height='100%' frameborder='0' src='https://www.youtube.com/embed/${value.embed}'></iframe>`;
  videoBlock.find('.informational-video_video-wrapper').html(videoEmbed);
  videoBlock.appendTo(infoVideo);
  if (value.sectionMarkers.length > 0) {
    $.each(value.sectionMarkers, (name, marker) => {
      $(`<div id=${marker}-video style='scroll-margin-top: 60px;'></div>`).insertBefore(videoBlock);
    });
  }
});

$('.informational-video_block:first').hide();
