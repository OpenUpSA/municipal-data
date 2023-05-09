import GroupedBarChartHoriz from 'municipal-money-charts/src/components/MunicipalCharts/GroupedBarChartHoriz';
import {
  logIfUnequal,
  formatForType,
} from '../utils.js';


class SpendingSection {
  constructor(selector, sectionData) {
    this.$element = $(selector);
    logIfUnequal(1, this.$element.length);
    this.sectionData = sectionData;
    this.$chartContainer = this.$element.find('.indicator-chart');
    this.$element.find('.video_download-button').attr('href', '/help#income-video');
  }
}

export class SpendingBreakdownSection extends SpendingSection {
  constructor(selector, sectionData) {
    super(selector, sectionData);
    this._initIndicator();
    this._initChart();
  }

  _initIndicator() {
    let value;
    if (this.sectionData.total === null) value = 'Not available';
    else value = formatForType('R', this.sectionData.total);
    this.$element.find('.indicator-metric__value').text(value);
  }

  _initChart() {
    if (this.sectionData.total === null) {
      this.$chartContainer.text('Data not available yet.');
    } else {
      this.chart = new GroupedBarChartHoriz(this.$chartContainer[0])
        .data(this.chartData());
    }
  }

  chartData() {
    // this is sample data
    return [
      {
        "category": "Property Rates",
        "values": [
          {
            "year": "2019",
            "value": 184331307
          },
          {
            "year": "2018",
            "value": 167951901
          },
          {
            "year": "2017",
            "value": 154311339
          },
          {
            "year": "2016",
            "value": 152512312
          }
        ]
      },
      {
        "category": "Service Charges",
        "values": [
          {
            "year": "2019",
            "value": 124331307
          },
          {
            "year": "2018",
            "value": 141513307
          },
          {
            "year": "2017",
            "value": 184331307
          },
          {
            "year": "2016",
            "value": 184331307
          }
        ]
      }
    ];
  }

  selectData(selection) {
    console.log('Not implemented');
  }
}