import { arrayJoin } from '../utils.js';

export class FormulaSection {
  constructor(selector, key, pageData) {
    this.selector = selector;
    this.key = key;
    this.sectionData = pageData.indicators[key];
    this.geography = pageData.geography;
    this.amountTypes = pageData.amount_types_v1;
    this.cubeNames = pageData.cube_names;
    this.$element = $(selector);

    this._initCalculation();
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
}
