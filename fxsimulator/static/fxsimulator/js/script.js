let socketio = io();

var options1 = {
    annotations: {
        yaxis: [{
            y: stock_data[stock_data.length - 1].y,
            borderColor: '#FF4560',
            width: '120%',
            label: {
                borderColor: '#FF4560',
                text: (stock_data[stock_data.length - 1].y).toFixed(3),
                offsetX: 48,
                offsetY: 6,
                style: {
                    background: '#FF4560',
                    color: '#fff',
                    fontSize: '8px',
                    fontWeight: 800
                }
            }
        }]
    },
    chart: {
        id: 'chart1',
        type: 'line',
        height: 230,
        animations: {
            enabled: true,
            easing: 'linear',
            speed: 400,
            animateGradually: {
                enabled: false,
                delay: 150
            },
            dynamicAnimation: {
                enabled: true,
                speed: 4500
            }
        },
        // toolbar: {
        //     show: true,
        //     offsetX: 0,
        //     offsetY: -10,
        //     tools: {
        //         download: false,
        //         selection: true,
        //         zoom: true,
        //         zoomin: true,
        //         zoomout: true,
        //         pan: true,
        //         reset: true | '<img src="/static/icons/reset.png" width="20">',
        //         customIcons: []
        //     },
        //     autoSelected: 'zoom'
        // }
        toolbar: {
            autoSelected: 'pan',
            show: 'false'
        }
    },
    datalables: {
        enabled: false
    },
    grid: {
        show: true,
    },
    series: [{
        name: 'Price',
        data: stock_data
    }],
    stroke: {
        width: 2
    },
    xaxis: {
        type: 'datetime',
        tickPlacement: 'between',
    },
    yaxis: [{
        seriesName: 'Price',
        axisTicks: {
            show: true,
            color: '#008FFB'
        },
        axisBorder: {
            show: true,
            color: '#008FFB'
        },
        labels: {
            style: {
                colors: '#008FFB',
            }
        },
        opposite: true,
        labels: {
            formatter: (value) => {
                return value.toFixed(0)}
        }
    }]
}

var chart1 = new ApexCharts(document.querySelector("#chart1"), options1);
chart1.render()

var options2 = {
    chart: {
        id: 'chart2',
        type: 'area',
        height: 130,
        brush: {
            target: 'chart1',
            enabled: true
        }
    },
    series: [{
        name: 'Price',
        data: stock_data
    }],
    // toolbar: {
    //     autoSelected: 'pan',
    //     show: false
    // },
    selection: {
        enabled: true,
        type: 'x',
        xaxis: {
            min: new Date(new Date() - 3600000),
            max: new Date()
        }
    },
    xaxis: {
        type: 'datetime',
        tooltip: {
            enabled: false
        }
    },
    yaxis: {
        tickAmount: 2,
        opposite: true,
        labels: {
            formatter: (value) => {
                return value.toFixed(0)}
        }
    }
}

var chart2 = new ApexCharts(document.querySelector("#chart2"), options2);
chart2.render()

socketio.on("message", (e) => {
    console.log(e);
    stock_data.push({
        x: e.date,
        y: e.close
    });

    animateCurrentPrice(e.open, e.close);
    chart1.updateSeries([{
        name: 'Price',
        data: stock_data
    }]);

    // chart.updateOptions({
    //     annotations: {
    //         yaxis: [{
    //             x: e.close,
    //         }]
    //     }
    // });

        //     chart1.updateOptions({
        //     annotations: {
        //         yaxis: [{
        //             y: e.close,
        //             borderColor: '#FF4560',
        //             width: '120%',
        //             label: {
        //                 borderColor: '#FF4560',
        //                 text: (stock_data[stock_data.length - 1].y).toFixed(3),
        //                 offsetX: 48,
        //                 offsetY: 6,
        //                 style: {
        //                     background: '#FF4560',
        //                     color: '#fff',
        //                     fontSize: '8px',
        //                     fontWeight: 800
        //                 }
        //             }
        //         }]
        //     },
        // });


    chart2.updateSeries([{
        name: 'Price',
        data: stock_data
    }]);
});

// Function to animate the current price smoothly to a new value
function animateCurrentPrice(startPrice, endPrice) {
    const startTime = new Date().getTime();
    const duration = 3000; // Duration for the animation (3 seconds)
    const startValue = startPrice;
    const change = endPrice - startPrice;

    function updateFrame() {
        const now = new Date().getTime();
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1); // Ensure progress is capped at 1

        const animatedPrice = startValue + change * progress;

        // Update the current price annotation

        if (now - startTime < duration) {
            requestAnimationFrame(updateFrame);
        } else {
            currentPrice = endPrice; // Update the current price to the final value
        }
    }

    updateFrame();
}