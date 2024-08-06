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
        text: 'Live EUR/USD'
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
    'wss://'
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


const time_input = document.querySelector('#time-input');
const amount_input = document.querySelector('#amount-input');

document.querySelector('#decrement-time-input').addEventListener("click", () => {
    if(time_input.value >= 2)
    {
        time_input.value--;
    }
    else{
        time_input.value=1;
    }
});
document.querySelector('#increment-time-input').addEventListener("click", () => {
    if(time_input.value <= 4)
    {
        time_input.value++;
    }
    else{
        time_input.value=5;
    }
});
document.querySelector('#decrement-amount-input').addEventListener("click", () => {
    if(amount_input.value >= 11)
    {
        amount_input.value--;
    }
    else{
        amount_input.value=10;
    }
});
document.querySelector('#increment-amount-input').addEventListener("click", () => {
    if (amount_input.value < 10)
    {
        amount_input.value = 10;
    }
    else if (amount_input.value <= 999)
    {
        amount_input.value++;
    }
    else{
        amount_input.value=10000;
    }
});
time_input.addEventListener("focusout", () => {
    if(time_input.value < 1)
    {
        time_input.value = 1;
    }
    else if(time_input.value > 5)
    {
        time_input.value = 5;
    }
});
amount_input.addEventListener("focusout", () => {
    if(amount_input.value < 10)
    {
        amount_input.value = 10;
    }
    else if(amount_input.value > 10000)
    {
        amount_input.value = 10000;
    }
});

document.querySelector("#down-button").addEventListener("click", () => {
    open_trade(false);
});

document.querySelector("#up-button").addEventListener("click", () => {
    open_trade(true);
});

const order_url = "https://" + window.location.host + "/fx/order/";

function open_trade(in_side){
    console.log(csrftoken)
    
    if( time_input.value >= 1 & time_input.value <=5 & amount_input.value >= 10 & amount_input.value <= 10000)
    {
        console.log(time_input.value)
        console.log(amount_input.value)
        console.log(in_side)
        
        order_data = {
            time : time_input.value,
            side : in_side,
            amount : amount_input.value
        }
        time_input.value = '';
        amount_input.value = '';

    }
    else {
        return;
    }
    
    fetch(order_url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(order_data),
      })
    .then(response => {
        if (!response.ok) 
        {
            throw new Error('Trade order error');
        }
        return response.json();
    })
    .then(order_response => {
        // Process the newly created user data
        console.log('Order Response Data:', order_response);
    })
    .catch(error => {
          console.error('Error:', error);
    });
}