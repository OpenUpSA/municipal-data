function amount_convert(value) {
  return `R ${value.toString()}`;
}
function sortCategories(a, b) {
  const categoryOrder = [
    'Indigent HH receiving FBS',
    'Affordable Range',
    'Middle Income Range',
  ];

  const indexA = categoryOrder.indexOf(a.name);
  const indexB = categoryOrder.indexOf(b.name);
  return indexA - indexB;
}
function overall_chart(container, chartData) {
  var data = [];
  let xaxis = [];
  for (const [income, value] of Object.entries(chartData)) {
    var region = {
      name: income,
      type: 'bar',
      y: value.y,
      x: value.x,
      hoverinfo: 'text',
      text: value.y.map(amount_convert),
    };
    xaxis = _.union(xaxis, value.x);
    data.push(region);
  }
  var layout = {
    barmode: 'group',
    xaxis: {
      categoryorder: 'array',
      categoryarray: xaxis.sort(),
    },
  };
  var config = { displayModeBar: false, responsive: true };

  data.sort(sortCategories);
  Plotly.newPlot(container, data, layout, config);
}

function income_chart(incomeData, container, yearly_percent) {
  var data = [];
  var lastIndex = -1;
  incomeData.forEach((item) => {
    var [service, value] = item;
    var region = {
      name: service,
      type: 'bar',
      y: value.y,
      x: value.x,
      hovertext: value.y.map(amount_convert),
      hovertemplate: '%{hovertext}<extra></extra>',
      textposition: 'outside',
      text: '',
      cliponaxis: false,
    };
    if (value.x.length > 0) {
      lastIndex += 1; // get the last stack
    }
    data.push(region);
  });
  var years = data[lastIndex].x;
  var percArr = [];
  for (var i = 0; i < years.length; i++) {
    var value = yearly_percent[years[i]];
    if (value !== '' && value !== '-' && value !== undefined) {
      percArr.push(`<b style="padding-top:5px">${value} %</b>`);
    } else {
      percArr.push('N/A');
    }
  }

  data[lastIndex].text = percArr;
  var layout = { barmode: 'stack' };
  var config = { responsive: true, displayModeBar: false };
  Plotly.newPlot(container, data, layout, config);
}
