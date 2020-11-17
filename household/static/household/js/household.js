function amount_convert(value){
    return 'R ' + value.toString();
}
function overall_chart(chartData){
    var data = [];
    var container = $("#income-over-time .indicator-chart")[0];
    for (const [income, value] of Object.entries(chartData)){
	var region = {
	    name: income,
	    type: 'bar',
	    y: value.y,
	    x:value.x,
	    hoverinfo:'text',
	    text: value.y.map(amount_convert),
	};
	data.push(region);
    }
    var layout = {barmode: 'group'};
    var config = {displayModeBar: false, responsive:true};
    Plotly.newPlot(container, data, layout, config);
}


function income_chart(incomeData, chart_id, yearly_percent){
    var data = [];
    var lastIndex = -1;
    for (const [service, value] of Object.entries(incomeData)){
	var region = {
	    name: service,
	    type: 'bar',
	    y: value.y,
	    x:value.x,
	    hovertext: value.y.map(amount_convert),
	    hovertemplate: '%{hovertext}<extra></extra>',
	    textposition: 'outside',
	    text:'',
	    cliponaxis: false,
	};
	if (value.x.length > 0) {
                lastIndex = lastIndex + 1;  //get the last stack
        }
	data.push(region);
    }
    var years = data[lastIndex].x;
    var percArr = [];
    for (var i = 0; i < years.length; i++) {
        var value = yearly_percent[years[i]];
        if (value !== '' && value !== '-') {
            percArr.push('<b style="padding-top:5px">' + value + ' %</b>');
        }
        else {
            percArr.push('N/A');
        }
    }

    data[lastIndex].text = percArr;
    var layout = {barmode: 'stack'};
    var config = {responsive:true, displayModeBar: false};
    Plotly.newPlot(chart_id, data, layout, config);
}
