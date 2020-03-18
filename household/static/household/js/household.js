function amount_convert(value){
    return 'R ' + value.toString();
}
function overall_chart(chartData){
    var data = [];   
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
    Plotly.newPlot('householdChart', data, layout, config);
}


function income_chart(incomeData, chart_id){
    var middleData = [];
    for (const [service, value] of Object.entries(incomeData)){
	var region = {
	    name: service,
	    type: 'bar',
	    y: value.y,
	    x:value.x,
	    hoverinfo:'text',
	    text: value.y.map(amount_convert),
	};
	middleData.push(region);
    }
    var layout = {barmode: 'stack'};
    var config = {responsive:true, displayModeBar: false};
    Plotly.newPlot(chart_id, middleData, layout);
}
