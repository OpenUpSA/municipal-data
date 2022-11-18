var mm = mm || {};
mm.BarChart = mm.BarChart || (function () {
  function BarChart() {}

  BarChart.prototype = {
    setupBar(el, text, val) {
      this.addTooltip(el, text);
      $('.bar', el).css('height', `${val}%`);
    },

    addTooltip(el, text) {
      $('.chart-tooltip', el).remove();
      var tooltip = $('<div></div>').addClass('chart-tooltip');
      ('.bar', el).append(tooltip);
      tooltip.append($('<div></div>').addClass('div-block-16'));
      tooltip.append($('<div></div>').addClass('text-block-5').text(text));
      tooltip.css('display', 'none');
      tooltip.css('visibility', 'visible');

      el.on('mouseover', (e) => {
        tooltip.show();
      })
        .on('mouseout', () => {
          tooltip.hide();
        });
    },
  };

  return BarChart;
}());
