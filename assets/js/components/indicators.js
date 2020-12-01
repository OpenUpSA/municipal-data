import { logIfUnequal, formatFinancialYear, ratingColor, formatForType } from '../utils.js';
import ColumnChart from './charts/column.js';
import ComparisonMenu from './comparison-menu';

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

    this.geography = geography;

    const chartContainerSelector = `${selector} .indicator-chart`;
    this.chart = new ColumnChart(chartContainerSelector, [this.chartData()]);
    const chartContainerParent = $(chartContainerSelector).parent();

    const $provinceButton = $(' <button class="button" style="display: unset"></button>');
    $provinceButton.text(` in ${geography.province_name}`);
    $provinceButton.on("click", (function() {
      this.chart.loadMedians(this.formatMedians().provincial);
    }).bind(this));

    const $nationalButton = $(' <button class="button" style="display: unset">nationally</button>');
    $nationalButton.on("click", (function() {
      this.chart.loadMedians(this.formatMedians().national);
    }).bind(this));


    const averageControls = $("<p></p>");
    averageControls.append('Show average for <a href="/help">similar municipalities</a> ');
    if (geography.category_name !== "metro municipality") {
      averageControls.append([
        $provinceButton,
        " or "
      ]);
    }
    averageControls.append($nationalButton);
    chartContainerParent.append(averageControls);


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
  comparisonChartData(profile) {
    return {
      "municipality": {
        "code": profile.demarcation.code,
        "name": "",
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

  updateComparisonButtons() {
  }

  updateChartComparison(comparisonOption) {
    if (comparisonOption === "none") {
      this.chart.loadData([this.chartData()]);
    } else {
      $.get(API_URL + '/cubes/municipalities/facts', (data) => {
        const miifGrouped  = _.groupBy(data.data, "municipality.miif_category");
        console.log(miifGrouped);
        let similarGroup = miifGrouped[this.geography.miif_category];
        similarGroup = similarGroup.filter(
          muni => muni["municipality.demarcation_code"] !== this.geography.geo_code
        );
        if (similarGroup) {
          console.log(similarGroup);
          const deferreds = _.sample(similarGroup, 3).map((muni) => {
            const demarcationCode = muni["municipality.demarcation_code"];
            const url = `/api/municipality-profile/${demarcationCode}/`;
            return $.get(url);
          });

          $.when(...deferreds).then(
            (...results) => {
              const comparisons = results.map(([result, textStatus, jqXHR]) => {
                return this.comparisonChartData(result);
              });
              this.chart.loadData([this.chartData(), ...comparisons]);
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
