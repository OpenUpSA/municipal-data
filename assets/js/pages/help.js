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
      xhosa: [['73.2 MB (Full size)', 'Municipal_Money%3A_Intro_to_Municipal_Finance_isiXhosa.mp4'], ['14.9 MB (Small size)', 'compressed/Municipal_Money%3A_Intro_to_Municipal_Finance_isiXhosa.mp4']],
      afr: [['82.5 MB (Full size)', 'Municipal_Money%3A_Intro_to_Municipal_Finance_Afrikaans.mp4'], ['14.7 MB (Small size)', 'compressed/Municipal_Money%3A_Intro_to_Municipal_Finance_Afrikaans.mp4']],
      sotho: [['76.9 MB (Full size)', 'Municipal_Money%3A_Intro_to_Municipal_Finance_Sotho.mp4'], ['14.2 MB (Small size)', 'compressed/Municipal_Money%3A_Intro_to_Municipal_Finance_Sotho.mp4']],
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
      videoBlock.find('.information-video_share-link').attr('href', `help#${marker}-video`);
    });
  }
});

$('.informational-video_block:first').hide();

$('.information-video_share-link').on('click', (e) => {
  e.preventDefault();
  navigator.clipboard.writeText(e.target.attributes[0].baseURI);
});

$('.informational-video_download-button').on('click', (e) => {
  const title = $(e.currentTarget.parentElement.parentElement.parentElement).find('.informational-video_title').text();
  const language = $(e.currentTarget.parentElement).find('.is-language-dropdown .dropdown__current-select').text();
  const size = $(e.currentTarget.parentElement).find('.is-size-dropdown .dropdown__current-select').text();
  gtag('event', 'video_download', {
    category: 'Video',
    action: 'Download',
    label: `${title} - ${language} - ${size}`,
  });
});

$('#features a').attr('href', `${DATA_PORTAL_URL}/docs#general`);

// Functional breakdown table
$("#features").append(
  `<section class="sub-section">
  <div id="func-breakdown-faq" class="sub-section__link"></div>
  <h3 class="heading">Spending functional breakdown</h3>
  <h4>Categorization of government functions</h4>
  <div target="_blank" class="rich-text is-space-below w-richtext">
    <table class="func-breakdown">
       <tr>
        <td><b>Category</b></td>
        <td><b>Function</b></td>
      </tr>
      <tr>
          <td>Community & Social Services</td>
          <td>
            Aged Care<br>
            Agricultural<br>
            Animal Care and Diseases<br>
            Cemeteries, Funeral Parlours and Crematoriums<br>
            Child Care Facilities<br>
            Civil Defence<br>
            Cleansing<br>
            Community Halls and Facilities<br>
            Consumer Protection<br>
            Control of Public Nuisances<br>
            Cultural Matters<br>
            Disaster Management<br>
            Education<br>
            Fencing and Fences<br>
            Fire Fighting and Protection<br>
            Indigenous and Customary Law<br>
            Industrial Promotion<br>
            Language Policy<br>
            Libraries and Archives<br>
            Licensing and Control of Animals<br>
            Literacy Programmes<br>
            Media Services<br>
            Museums and Art Galleries<br>
            Police Forces, Traffic and Street Parking Control<br>
            Population Development<br>
            Pounds<br>
            Provincial Cultural Matters<br>
            Theatres<br>
            Zoo's
          </td>
      </tr>
      <tr>
          <td>Electricity</td>
          <td>Electricity<br>Street Lighting and Signal Systems</td>
      </tr>
      <tr>
          <td>Environmental Protection</td>
          <td>Biodiversity and Landscape<br>Coastal Protection<br>Indigenous Forests<br>Nature Conservation<br>Pollution Control<br>Soil Conservation</td>
      </tr>
      <tr>
          <td>Governance, Administration, Planning and Development</td>
          <td>
            Administrative and Corporate Support<br>
            Asset Management<br>
            Billboards<br>Central City Improvement District<br>
            Corporate Wide Strategic Planning (IDPs, LEDs)<br>
            Development Facilitation<br>
            Economic Development/Planning<br>
            Finance<br>
            Fleet Management<br>
            Governance Function<br>
            Human Resources<br>
            Information Technology<br>
            Legal Services<br>
            Licensing and Regulation<br>
            Marketing, Customer Relations, Publicity and Media Co-ordination<br>
            Mayor and Council<br>
            Municipal Manager, Town Secretary and Chief Executive<br>
            Project Management Unit<br>
            Property Services<br>
            Provincial Planning<br>
            Regional Planning and Development<br>
            Risk Management<br>
            Security Services<br>
            Supply Chain Management<br>
            Support to Local Municipalities<br>
            Town Planning, Building Regulations and Enforcement, and City Engineer<br>
            Valuation Service
          </td>
      </tr>
      <tr>
          <td>Health</td>
          <td>
            Ambulance<br>
            Chemical Safety<br>
            Food Control<br>
            Health Services<br>
            Health Surveillance and Prevention of Communicable Diseases including immunizations<br>
            Laboratory Services<br>
            Vector Control
          </td>
      </tr>
      <tr>
          <td>Housing</td>
          <td>Housing<br>Informal Settlements</td>
      </tr>
      <tr>
          <td>Other</td>
          <td>Abattoirs<br>Air Transport<br>Forestry<br>Markets<br>Nonelectric Energy<br>Tourism</td>
      </tr>
      <tr>
          <td>Road Transport</td>
          <td>Public Transport<br>Road and Traffic Regulation<br>Roads<br>Taxi Ranks</td>
      </tr>
      <tr>
          <td>Sport And Recreation</td>
          <td>Beaches and Jetties<br>Casinos, Racing, Gambling, Wagering<br>Community Parks (including Nurseries)<br>Recreational Facilities<br>Sports Grounds and Stadiums</td>
      </tr>
      <tr>
          <td>Waste Management</td>
          <td>Recycling<br>Solid Waste Disposal (Landfill Sites)<br>Solid Waste Removal<br>Street Cleaning</td>
      </tr>
      <tr>
          <td>Waste Water Management</td>
          <td>Public Toilets<br>Sewerage<br>Storm Water Management<br>Waste Water Treatment</td>
      </tr>
      <tr>
          <td>Water</td>
          <td>Water Distribution<br>Water Storage<br>Water Treatment</td>
      </tr>
    </table>
  </div>
  </section>
  <style>
    .func-breakdown td {
      vertical-align: top;
    }
  </style>`
);
