$(function () {
    $('#lottery_1').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        credits: { 
            enabled: false 
        },
        exporting: {
            enabled: false
        },
        tooltip: {
            enabled: false
        },
        title: {
            text: '',
        },
        plotOptions: {
            pie: {
                size: '100%',
                allowPointSelect: false,
                animation: false,
                dataLabels: {
                    enabled: true,
                    distance: -40,
                    format: '{point.x}',
                    color: 'black',
                    style: {
                        textShadow: false,
                        fontSize: "20px"
                    }
                },
                states: {
                   hover: {
                       enabled: false
                   }
               }
            }
        },
        series: [{
            name: 'Auszahlung',
            colorByPoint: true,
            data: [{
                name: 'Right',
                color: '#6495ED',
                y: 50,
                x: 100
            }, {
                name: 'Left',
                color: 'GreenYellow',
                y: 50,
                x: 20
            }]
        }]
    });
});