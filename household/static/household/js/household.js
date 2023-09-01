function amount_convert(value) {
  return `R ${value.toString()}`;
}
function sortByClass(classMap) {
  return function (a, b) {
    const indexA = classMap.findIndex((obj) => obj.name === a.name);
    const indexB = classMap.findIndex((obj) => obj.name === b.name);

    if (indexA !== -1) {
      a.name = classMap[indexA].chartKey;
    }
    if (indexB !== -1) {
      b.name = classMap[indexB].chartKey;
    }
    return indexA - indexB;
  };
}
function sortByClass2(classMap) {
  return function (a, b) {
    const indexA = classMap.findIndex((obj) => obj.name === a.name);
    const indexB = classMap.findIndex((obj) => obj.name === b.name);

    if (indexA !== -1) {
      a.name = classMap[indexA].chartKey;
      a.color = classMap[indexA].barColor.color;
    }
    if (indexB !== -1) {
      b.name = classMap[indexB].chartKey;
      b.color = classMap[indexB].barColor.color;
    }
    return indexA - indexB;
  };
}
function overall_chart(container, chartData) {
  var data = [];
  let xaxis = [];
  const classMap = [
    { name: 'Indigent HH receiving FBS', chartKey: 'Indigent (Example A)', barColor: { color: 'rgb(0, 166, 81)' } },
    { name: 'Affordable Range', chartKey: 'Affordable (Example B)', barColor: { color: 'rgb(251, 176, 59)' } },
    { name: 'Middle Income Range', chartKey: 'Middle Income (Example C)', barColor: { color: 'rgb(237, 28, 36)' } },
  ];

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

    classMap.forEach((item) => {
      if (item.name == income) {
        region.marker = item.barColor;
      }
    });
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
  data.sort(sortByClass(classMap));
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
