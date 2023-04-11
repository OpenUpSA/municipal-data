import ColumnChart from 'municipal-money-charts/src/components/MunicipalCharts/ColumnChart.js';
import {
  arrayJoin,
  logIfUnequal,
  formatFinancialYear,
  ratingColor,
  formatForType,
} from '../utils.js';
import ComparisonMenu from './comparison-menu';
import 'core-js/stable';
import 'regenerator-runtime/runtime';

const indicatorMetricClass = {
  good: '.indicator-metric--status-green',
  ave: '.indicator-metric--status-yellow',
  bad: '.indicator-metric--status-red',
  '': '.indicator-metric--no-status',
};

const miifCategoryMap = {
  'A': 'metro',
  'B': 'local',
  'C': 'district',
};

function comparePeriod(a, b) {
  if (a.period < b.period) {
    return -1;
  }
  if (a.period > b.period) {
    return 1;
  }
  return 0;
}

export class IndicatorSection {
  constructor(selector, key, pageData) {
    this.selector = selector;
    this.key = key;
    this.sectionData = pageData.indicators[key];
    this.medians = pageData.medians[key];
    this.geography = pageData.geography;
    this.amountTypes = pageData.amount_types_v1;
    this.cubeNames = pageData.cube_names;
    this.municipalCategoryDescriptions = pageData.municipal_category_descriptions;
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.latestItem = this.sectionData.values[0];
    this.comparisons = [];

    const chartContainerSelector = `${this.selector} .indicator-chart`;
    this.chart = new ColumnChart(chartContainerSelector, [this.chartData()]);
    this.chartContainer = $(chartContainerSelector);
    this.chartContainer.addClass('column-chart');
    this.chartContainerParent = $(chartContainerSelector).parent();

    this._initAverageButtons();
    this._initComparisonButtons();
    this._initCategoryInfo();
    this._initCalculation();
    this._initSectionPeriod();
    this._initMetric();
    this._initEvents();

    this.comparisonMenu = new ComparisonMenu(selector, this.key);
    this.comparisonMenu.$element.on('option-select', ((e) => {
      this.updateChartComparison(e.detail.option);
    }));

    this.$element.on('click-col', ((e) => {
      const containerId = $(e.currentTarget).attr('class');
      const buttonId = $(e.target).attr('colid');
      $(`.${containerId} .chart-btn`).removeClass('active');
      $(`.${containerId} [data-muni=${buttonId}]`).addClass('active');
    }));
  }

  formatMetric(value) {
    if (value || value === 0) {
      return formatForType(this.sectionData.result_type, value);
    }

    return 'Not available';
  }

  _initEvents() {
    $(`${this.selector} .expand-block`).on('click', ((e) => {
      gtag('event', 'more_info', {
        category: 'More info',
        action: 'Expand',
        label: `${this.key} ${$(e.target).text()}`,
      });
    }));

    $(`${this.selector} .indicator-calculation__formula-actual`).on('click', ((e) => {
      gtag('event', 'formula_click', {
        category: 'Formulas',
        action: 'Follow link',
        label: `${this.key} ${$(e.target).text()}`,
      });
    }));
  }

  _initCategoryInfo() {
    const miifCategory = this.geography.miif_category;
    const categoryName = this.geography.category_name;
    const $category = this.$element.find('.muni-type__wrapper');
    const $label = $category.find('.label');
    const $description = $category.find('.tooltip__description');
    const $link = $category.find('.tooltip__link');
    $label.text(`category ${miifCategory} ${miifCategoryMap[this.geography.category]} municipalities`);
    $description.text(this.municipalCategoryDescriptions[miifCategory]);
    $link.attr('href', '/help#similar-munis');
    this.$element.find('.video_download-button').attr('href', `/help#${this.selector.substring(1)}-video`);
  }

  _initCalculation() {
    // Render the calculation reference
    const referenceData = this.sectionData.ref;
    const $referenceEl = this.$element.find('.indicator-calculation__reference');
    if ($referenceEl.length && referenceData) {
      const $el = $('<a></a>');
      $el.attr('href', referenceData.url);
      $el.text(referenceData.title);
      $referenceEl.append($el);
    }
    // Render the formula data
    const formulaDataV2 = this.sectionData.formula_v2;
    const formulaData = this.sectionData.formula;

    // Hide unused formula elements
    if (this.sectionData.last_year <= 2019) {
      this.$element.find('.is--post-2019-20').hide();
      this.$element.find('.indicator-calculation__heading').hide();
    }
    if (this.sectionData.last_year >= 2023) {
      this.$element.find('.is--pre-2019-20').hide();
      this.$element.find('.indicator-calculation__heading').hide();
    }

    if (formulaDataV2) {
      const textData = formulaDataV2.text;
      const $textEl = this.$element.find('.indicator-calculation__formula-text');
      if ($textEl.length && textData) {
        $textEl.text(textData);
      }
      this.setFormulaLink(formulaDataV2, '.indicator-calculation__formula-actual.is--post-2019-20', this.sectionData.last_year);
    }

    if (formulaData) {
      const textData = formulaData.text;
      const $textEl = this.$element.find('.indicator-calculation__formula-text');
      if ($textEl.length && textData) {
        $textEl.text(textData);
      }
      this.setFormulaLink(formulaData, '.indicator-calculation__formula-actual.is--pre-2019-20', '2019');
    }
  }

  _initSectionPeriod() {
    this.$element.find('.section-header__info-right').text(this.formatPeriod(this.latestItem.date));
  }

  _initMetric() {
    const $skeleton = this.$element.find('.indicator-metric');
    logIfUnequal(1, $skeleton.length);
    const templateClass = indicatorMetricClass[this.latestItem.rating];
    const $element = $(`.components ${templateClass}`).clone();
    logIfUnequal(1, $element.length);
    const value = this.formatMetric(this.latestItem.result);
    $element.find('.indicator-metric__value').text(value);
    $skeleton.hide();
    $element.insertBefore($skeleton);
    $skeleton.remove();
  }

  setFormulaLink(formulaData, container, last_year) {
    const { geo_code } = this.geography;
    const actualData = formulaData.actual;

    const $actualEl = this.$element.find(container);
    if ($actualEl.length && actualData) {
      const components = Object.values(actualData).map((data) => {
        if (typeof data === 'string') {
          return data;
        }
        const $el = $('<a></a>');
        let params = {};
        let text = '';
        const cube_name = this.cubeNames[data.cube];
        let { amount_type } = data;
        amount_type = this.amountTypes[amount_type] || amount_type;
        // Set the query parameters
        params.municipalities = geo_code;
        params.year = last_year;
        params.items = data.item_codes;

        if (data.amount_type) {
          params.amountType = data.amount_type;
        }
        // Generate the text
        text += `[${cube_name}]`;
        if (data.item_description !== undefined && data.item_description !== '') {
          text += ` ${data.item_description}`;
        } else {
          text += ` item code ${data.item_codes.join(', ')}`;
        }
        if (data.amount_type) {
          text += `, ${amount_type}`;
        }
        params = new URLSearchParams(params).toString();
        const url = `${DATA_PORTAL_URL}/table/${data.cube}/?${params}`;
        $el.text(text);
        $el.attr('href', url);
        return $el;
      });
      // Append the components to the element
      $actualEl.append(arrayJoin(components, '&nbsp;'));
    }
  }

  chartData() {
    const items = this.sectionData.values.map((item) => ({
      period: this.formatPeriod(item.date),
      fillColor: ratingColor(item.rating),
      value: item.result,
    }));
    items.reverse();
    return {
      municipality: {
        code: this.geography.geo_code,
        name: this.geography.short_name,
        province_code: this.geography.province_code,
      },
      data: items,
      resultType: this.resultType(),
    };
  }

  comparisonChartData(profile, muni) {
    return {
      municipality: {
        code: profile.demarcation.code,
        name: muni.name,
        province_code: muni.province_code,
      },
      data: profile.indicators[this.key].values.map((period) => ({
        period: this.formatPeriod(period.date),
        fillColor: '#ccc',
        value: period.result,
      })),
    };
  }

  formatMedians() {
    const national = Object.entries(this.medians.national.dev_cat).map(([key, value]) => ({
      period: this.formatPeriod(key),
      value,
    }));
    const provincial = Object.entries(this.medians.provincial.dev_cat).map(([key, value]) => ({
      period: this.formatPeriod(key),
      value,
    }));
    national.sort(comparePeriod);
    provincial.sort(comparePeriod);
    return {
      national,
      provincial,
    };
  }

  resultType() {
    return {
      R: 'currency',
      '%': 'percentage',
    }[this.sectionData.result_type] || this.sectionData.result_type;
  }

  formatSpecifier() {
    return {
      R: '$,.0f',
    }[this.sectionData.result_type];
  }

  formatValue(value) {
    return locale.format(this.formatSpecifier())(value);
  }

  formatPeriod(period) {
    return formatFinancialYear(period);
  }

  _initAverageButtons() {
    const $provinceButton = $(' <button class="button" style="display: unset"></button>');
    $provinceButton.text(` in ${this.geography.province_name}`);
    $provinceButton.on('click', (() => {
      this.chart.loadMedians(this.formatMedians().provincial);
      ga('send', 'event', 'chart-averages', `${this.key} provincial`);
      gtag('event', 'chart_averages', {
        category: 'Charts',
        action: 'Show averages',
        label: `${this.key} provincial`,
      });
    }));

    const $nationalButton = $(' <button class="button" style="display: unset">nationally</button>');
    $nationalButton.on('click', (() => {
      this.chart.loadMedians(this.formatMedians().national);
      ga('send', 'event', 'chart-averages', `${this.key} national`);
      gtag('event', 'chart_averages', {
        category: 'Charts',
        action: 'Show averages',
        label: `${this.key} national`,
      });
    }));

    const averageControls = $('<p></p>');
    averageControls.append('Show average for <a href="/help#similar-munis">similar municipalities</a> ');
    if (this.geography.category_name !== 'metro municipality') {
      averageControls.append([
        $provinceButton,
        ' or ',
      ]);
    }
    averageControls.append($nationalButton);
    this.chartContainerParent.append(averageControls);
  }

  _initComparisonButtons() {
    this.comparisonButtonsContainer = $('<p></p>');
    this.comparisonButtonsContainer.insertBefore(this.chartContainer);

    this.getSimilarMunis('similar-same-province').then((similarProv) => {
      if (similarProv.length > 0) {
        this.$element.find('.w-dropdown-list a[data-option=similar-same-province]').removeClass('dropdown-link--disabled');
        this.$element.find('.w-dropdown-list a[data-option=similar-same-province]').css('pointer-events', 'initial');
      }
    });
  }

  highlightComparisonButton(container, muniId) {
    $(`${container} .chart-btn`).removeClass('active');
    $(`${container} #${muniId}`).addClass('active');
  }

  _updateComparisonButtons() {
    this.comparisonButtonsContainer.empty();
    this.comparisonButtonsContainer.append('Comparing ');
    [this.chartData(), ...(this.comparisons)].forEach((comparison) => {
      const button = $(` <button data-muni="${comparison.municipality.code}"class="button chart-btn"></button> `);
      button.click(() => {
        this.highlightComparisonButton(this.selector, comparison.municipality.code);
        this.chart.highlightCol(comparison.municipality.code);
        ga('send', 'event', 'chart-compare-highlight', `${this.key} ${comparison.municipality.code}`);
        gtag('event', 'chart_compare_highlight', {
          category: 'Charts',
          action: 'Click municipality columns',
          label: `${this.key} ${comparison.municipality.code}`,
        });
      });
      button.text(`${comparison.municipality.name}, ${comparison.municipality.province_code}`);
      this.comparisonButtonsContainer.append(button);
    });
  }

  async getSimilarMunis(comparisonOption) {
    try {
      const response = await $.ajax({
        url: '/api/geography/geography/',
      });

      const activeMunicipalities = response.filter((obj) => obj.is_disestablished !== true);
      const miifGrouped = _.groupBy(activeMunicipalities, 'miif_category');
      let similarGroup = miifGrouped[this.geography.miif_category];
      // Remove current muni from selection
      similarGroup = similarGroup.filter(
        (muni) => muni.geo_code !== this.geography.geo_code,
      );

      let groups;
      if (comparisonOption === 'similar-nearby') {
        groups = _.groupBy(_.toArray(similarGroup), 'parent_code');
        similarGroup = groups[this.geography.parent_code];
      } else if (comparisonOption === 'similar-same-province') {
        groups = _.groupBy(similarGroup, 'province_code');
        similarGroup = groups[this.geography.province_code];
      } else if (comparisonOption === 'similar-nationally') {
      } else {
        console.error('unsupported comparisonOption', comparisonOption);
      }
      return similarGroup || [];
    } catch (error) {
      console.error(error);
      alert('Error looking up similar municipalities. Please try again.');
      return [];
    }
  }

  updateChartComparison(comparisonOption) {
    if (comparisonOption === 'none') {
      this.chart.loadData([this.chartData()]);
    } else {
      this.getSimilarMunis(comparisonOption).then((similarGroup) => {
        if (similarGroup.length > 0) {
          const sampleMunis = _.sample(similarGroup, 3);
          const deferreds = sampleMunis.map((muni) => {
            const demarcationCode = muni.geo_code;
            const url = `/api/municipality-profile/${demarcationCode}/`;
            return $.get(url);
          });

          Promise.all(deferreds)
            .then((results) => {
              this.comparisons = results.map((result, index) => this.comparisonChartData(result, sampleMunis[index]));
              this.chart.loadData([this.chartData(), ...(this.comparisons)]);
              this._updateComparisonButtons();
            })
            .catch((details) => {
              console.error('Error fetching comparison data: ', details);
              alert('Error loading comparison data. Please try again.');
            });
        } else {
          alert('Unfortunately there are no similar municipalities for the selection. Please try again.');
        }
      });
    }
  }
}

export class OverUnderSection extends IndicatorSection {
  formatMetric(value) {
    const overunder = value > 0 ? 'overspent' : 'underspent';
    return `${super.formatMetric(Math.abs(value))} ${overunder}`;
  }
}
