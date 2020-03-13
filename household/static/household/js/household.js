function overall_chart(chartData){
    var data = [];   
    for (const [income, value] of Object.entries(chartData)){
	var region = {
	    name: income,
	    type: 'bar',
	    y: value.x,
	    x:value.y,
	    text: value.y.map(String),
	    textposition: 'auto',
	    hoverinfo:'none',
	    orientation: 'h'
	};
	data.push(region);
    }
    var layout = {barmode: 'group', font:{size: 18}};
    var config = {displayModeBar: false, responsive:true};
    Plotly.newPlot('householdChart', data, layout, config);
}


function income_chart(incomeData, chart_id){
    var middleData = [];
    console.log(incomeData);
    for (const [service, value] of Object.entries(incomeData)){
	var region = {
	    name: service,
	    type: 'bar',
	    y: value.y,
	    x:value.x,
	};
	middleData.push(region);
    }
    var layout = {barmode: 'stack'};
    //var config = {displayModeBar: false, responsive:true}
    Plotly.newPlot(chart_id, middleData, layout);
}
