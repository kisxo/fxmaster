let stock_data = [[1234567890000, 300]]

const chart = Highcharts.stockChart('container', {
    chart: {
        events: {
            load: function () {
                this.xAxis[0].update({
                    overscroll: 1000 * 10
                })
            }
        },
    },
    credits: {
        enabled: false
    },
    accessibility: {
        enabled: false
    },
    time: {
        useUTC: true
    },
    rangeSelector: {
        buttons: [{
            count: 1,
            type: 'minute',
            text: '1M'
        }, {
            count: 5,
            type: 'minute',
            text: '5M'
        }, {
            type: 'all',
            text: 'All'
        }],
        inputEnabled: false,
        selected: 0
    },
    title: {
        text: 'Live random data'
    },
    exporting: {
        enabled: false
    },
    series: [{
        type: 'line',
        name: 'Price',
        data: stock_data,
        // color: '#FF7F7F',
        // upColor: '#90EE90',
        lastPrice: {
            color: '#FF7F7F',
            enabled: true,
            label: {
                enabled: true,
                backgroundColor: '#FF7F7F',
                formatter: (value) => {
                    return value.toFixed(1);
                },
                padding: 4,
                shape: 'callout',
                style: {
                    "fontWeight": "bold"
                }
            }
        }
    }],
    xAxis: {
        type: 'datetime',
        events: {
            afterSetExtremes: function (e) {
                var chart = this.chart,
                range = e.max - e.min,
                overscrollValue;

                // Set overscroll value based on the zoom level (range)
                if (range > 1000 * 60 * 5) {
                    // Greater than 5 min
                    overscrollValue = (range / 100) * 15; // 15 %
                } else if (range > 1000 * 60 * 1) {
                    // Greater than a min
                    overscrollValue = 1000 * 60 * 1; // 1min
                } else {
                    overscrollValue = 1000 * 10; // 10 seccond
                }
                chart.xAxis[0].update({
                    overscroll: overscrollValue
                });
            }
        },
    },
    yAxis: {
        minPadding: .2,
        maxPadding: .2
    }
});

// socketio.on("message", (e) => {
//     console.log(e)
//     chart.series[0].addPoint([e.period, e.price], true, false, {
//         duration: 4000,
//         easing: 'linear'
//     });
// });

console.log(stock_data);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/fxupdatechannel/fxupdateroom/'
);

chatSocket.onmessage = function(e) {
    const response = JSON.parse(e.data);
    console.log(response);
    chart.series[0].addPoint([response.data.period, response.data.price], true, false, {
         duration: 4000,
         easing: 'linear'
     });
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};