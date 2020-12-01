import { logIfUnequal, formatFinancialYear, ratingColor, formatForType } from '../utils.js';
import ColumnChart from './charts/column.js';
import ComparisonMenu from './comparison-menu';
import "core-js/stable";
import "regenerator-runtime/runtime";

const indicatorMetricClass = {
  "good": ".indicator-metric--status-green",
  "ave": ".indicator-metric--status-yellow",
  "bad": ".indicator-metric--status-red",
  "": ".indicator-metric--no-status",
};

function comparePeriod( a, b ) {
  if ( a.period < b.period ){
    return -1;
  }
  if ( a.period > b.period ){
    return 1;
  }
  return 0;
}

export class IndicatorSection {
  constructor(selector, key, sectionData, medians, geography) {
    this.selector = selector;
    this.key = key;
    this.sectionData = sectionData;
    this.medians = medians;
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.latestItem = sectionData.values[0];
    this.comparisons = [];

    this.geography = geography;

    const chartContainerSelector = `${this.selector} .indicator-chart`;
    this.chart = new ColumnChart(chartContainerSelector, [this.chartData()]);
    this.chartContainer = $(chartContainerSelector);
    this.chartContainerParent = $(chartContainerSelector).parent();

    this._initAverageButtons();
    this._initComparisonButtons();

    this.initSectionPeriod();
    this.initMetric();

    this.comparisonMenu = new ComparisonMenu(selector);
    this.comparisonMenu.$element.on("option-select", ((e) => {
      this.updateChartComparison(e.detail.option);
    }).bind(this));
  }

  formatMetric(value) {
    return formatForType(this.sectionData.result_type, value);
  }

  initSectionPeriod() {
    this.$element.find(".section-header__info-right").text(this.formatPeriod(this.latestItem.date));
  }

  initMetric() {
    const $skeleton = this.$element.find(".indicator-metric");
    logIfUnequal(1, $skeleton.length);
    const templateClass = indicatorMetricClass[this.latestItem.rating];
    const $element = $(`.components ${templateClass}`).clone();
    logIfUnequal(1, $element.length);
    const value = this.formatMetric(this.latestItem.result);
    $element.find(".indicator-metric__value").text(value);
    $skeleton.hide();
    $element.insertBefore($skeleton);
    $skeleton.remove();
  }

  chartData() {
    const items = this.sectionData.values.map((item) => {
      return {
        period: this.formatPeriod(item.date),
        fillColor: ratingColor(item.rating),
        value: item.result,
      };
    });
    items.reverse();
    return {
      municipality: {
        code: this.geography.geo_code,
        name: this.geography.short_name,
      },
      data: items,
      resultType: this.resultType(),
    };
  }
  comparisonChartData(profile, muni) {
    return {
      "municipality": {
        "code": profile.demarcation.code,
        "name": muni["municipality.name"],
      },
      "data": profile.indicators[this.key].values.map(period => {
        return {
          "period": this.formatPeriod(period.date),
          "fillColor": "#ccc",
          "value": period.result,
        };
      }),
    };
  }

  formatMedians() {
    const national = Object.entries(this.medians.national.dev_cat).map(([key, value]) => {
      return {
        period: this.formatPeriod(key),
        value: value,
      };});
    const provincial = Object.entries(this.medians.provincial.dev_cat).map(([key, value]) => {
      return {
        period: this.formatPeriod(key),
        value: value,
      };});
    national.sort(comparePeriod);
    provincial.sort(comparePeriod);
    return {
      national: national,
      provincial: provincial,
    };
  }

  resultType() {
    return {
      "R": "currency",
      "%": "percentage",
    }[this.sectionData.result_type] || this.sectionData.result_type;
  }

  formatSpecifier() {
    return {
      "R": "$,.0f",
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
    $provinceButton.on("click", (function() {
      this.chart.loadMedians(this.formatMedians().provincial);
    }).bind(this));

    const $nationalButton = $(' <button class="button" style="display: unset">nationally</button>');
    $nationalButton.on("click", (function() {
      this.chart.loadMedians(this.formatMedians().national);
    }).bind(this));


    const averageControls = $("<p></p>");
    averageControls.append('Show average for <a href="/help">similar municipalities</a> ');
    if (this.geography.category_name !== "metro municipality") {
      averageControls.append([
        $provinceButton,
        " or "
      ]);
    }
    averageControls.append($nationalButton);
    this.chartContainerParent.append(averageControls);

  }

  _initComparisonButtons() {
    this.comparisonButtonsContainer = $("<div></div>");
    this.comparisonButtonsContainer.insertBefore(this.chartContainer);
  }

  _updateComparisonButtons() {
    this.comparisonButtonsContainer.empty();
    this.comparisonButtonsContainer.append("Comparing ");
    [this.chartData(), ...this.comparisons].forEach((comparison) => {
      const button = $(' <button class="button" style="display: unset; margin: 2px 2px"></button> ');
      button.click(() => {
        this.chart.resetHighlight();
        this.chart.highlightCol(comparison.municipality.code);
      });
      button.text(comparison.municipality.name);
      this.comparisonButtonsContainer.append(button);
    });
  }

  async getSimilarMunis() {
    try {
      const response = await $.ajax({
        url: API_URL + '/cubes/municipalities/facts'
      });
      const miifGrouped  = _.groupBy(response.data, "municipality.miif_category");
      let similarGroup = miifGrouped[this.geography.miif_category];
      similarGroup = similarGroup.filter(
        muni => muni["municipality.demarcation_code"] !== this.geography.geo_code
      );
      return similarGroup;
    } catch (error) {
      console.log(error);
      alert("Error looking up similar municipalities. Please try again.");
      return [];
    }
  }

  updateChartComparison(comparisonOption) {
    if (comparisonOption === "none") {
      this.chart.loadData([this.chartData()]);
    } else {
      this.getSimilarMunis().then((similarGroup) => {
        if (similarGroup.length > 0) {
          const sampleMunis = _.sample(similarGroup, 3);
          const deferreds = sampleMunis.map((muni) => {
            const demarcationCode = muni["municipality.demarcation_code"];
            const url = `/api/municipality-profile/${demarcationCode}/`;
            return $.get(url);
          });

          $.when(...deferreds).then(
            (...results) => {
              this.comparisons = results.map(([result, textStatus, jqXHR], index) => {
                return this.comparisonChartData(result, sampleMunis[index]);
              });
              this.chart.loadData([this.chartData(), ...this.comparisons]);
              this._updateComparisonButtons();
            },
            (...details) => {
              console.error("Error fetching comparison data", ...details);
              alert("Error loading comparison data. Please try again.");
            });
        } else {
          alert("Unfortunately there are no similar municipalities");
        }
      });
    }
  }
}

export class OverUnderSection extends IndicatorSection {
  formatMetric(value) {
    const overunder = value > 0 ? "overspent" : "underspent";
    return `${super.formatMetric(value)} ${overunder}`;
  }
}
