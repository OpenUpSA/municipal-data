import GroupedBarChartHoriz from 'municipal-money-charts/src/components/MunicipalCharts/GroupedBarChartHoriz';


class SpendingSection {
  constructor(selector, sectionData) {
    this.$element = $(selector);
    this.sectionData = sectionData;
    this.$chartContainer = this.$element.find('.indicator-chart');
  }
}

export class SpendingBreakdownSection extends SpendingSection {
  constructor(selector, sectionData) {
    super(selector, sectionData);
    this._initChart();
  }

  _initChart() {
    this.$element.find('.financial-period').text('');
    if (this.sectionData.total === null) {
      this.$chartContainer.text('Data not available yet.');
    } else {
      this.chart = new GroupedBarChartHoriz(this.$chartContainer[0])
        .data(this.chartData());
    }
  }

  chartData() {
    return (this.sectionData.values);
  }
}