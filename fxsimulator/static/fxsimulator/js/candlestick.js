let chartData = [];
let currentPrice = null;
let chart;

// Function to create the ApexCharts chart
function createChart() {
    let options = {
        series: [{
            data: chartData
        }],
        chart: {
            type: 'candlestick',
            height: 350,
            animations: {
                enabled: true,
                easing: 'linear', // Set easing to linear for smoother animation
                speed: 800 // Adjust animation speed as needed
            }
        },
        title: {
            text: 'Real-time 1-Minute Candlestick Chart',
            align: 'left'
        },
        xaxis: {
            type: 'datetime',
            labels: {
                formatter: function (value) {
                    return new Date(value).toLocaleTimeString(); // Example formatting for x-axis
                }
            }
        },
        yaxis: {
            tooltip: {
                enabled: true
            },
            labels: {
                formatter: function (value) {
                    return value.toFixed(3); // Display three digits after the decimal point for y-axis labels
                }
            },
            // Set a fixed range for the y-axis
            min: function (min) {
                return Math.min(min, currentPrice - 10); // Adjust to your preference
            },
            max: function (max) {
                return Math.max(max, currentPrice + 10); // Adjust to your preference
            }
        },
        annotations: {
            yaxis: [{
                x: null, // Initial x value for current price annotation (will be set dynamically)
                y: null, // Initial y value for current price annotation
                borderColor: '#FF4560',
                label: {
                    borderColor: '#FF4560',
                    style: {
                        color: '#fff',
                        background: '#FF4560'
                    },
                    text: 'Current Price'
                }
            }]
        }
    };

    chart = new ApexCharts(document.querySelector("#candlestickChart"), options);
    chart.render();
}

// Placeholder for 5-second data points
let tempData = [];

// Function to generate new 5-second data (simulate fetching from an API)
function generate5SecData() {
    const now = new Date();
    const open = tempData.length > 0 ? tempData[tempData.length - 1][4] : 100 + Math.random() * 10;
    const close = open + Math.random() * 2 - 1;
    const high = Math.max(open, close) + Math.random();
    const low = Math.min(open, close) - Math.random();

    return [now.getTime(), open, high, low, close];
}

// Function to aggregate 5-second data into a 1-minute candle
function aggregateTo1Minute() {
    if (tempData.length === 0) return;
    
    const time = tempData[0][0];
    const open = tempData[0][1];
    const close = tempData[tempData.length - 1][4];
    const high = Math.max(...tempData.map(d => d[2]));
    const low = Math.min(...tempData.map(d => d[3]));

    const newCandle = {
        x: time,
        y: [open, high, low, close]
    };

    chartData.push(newCandle);
    currentPrice = close;

    // Clear temporary data
    tempData = [];

    // Update the chart with the new data
    chart.updateSeries([{ data: chartData }], true);

    // Update y-axis range to ensure current price is visible
    chart.updateOptions({
        yaxis: {
            tooltip: {
                enabled: true
            },
            labels: {
                formatter: function (value) {
                    return value.toFixed(3); // Display three digits after the decimal point for y-axis labels
                }
            },
            min: currentPrice - 10, // Adjust to your preference
            max: currentPrice + 10 // Adjust to your preference
        }
    });

    // Update current price annotation position to the extreme right
    const lastCandle = chartData[chartData.length - 1];
    const annotationX = lastCandle ? lastCandle.x : null;

    chart.updateOptions({
        annotations: {
            yaxis: [{
                x: annotationX,
                y: currentPrice,
                label: {
                    text: `Current Price: ${currentPrice.toFixed(3)}`
                }
            }]
        }
    });
}

// Function to update the chart with new 5-second data and animate the current price smoothly to the new price
function updateChart() {
    const new5SecData = generate5SecData();
    tempData.push(new5SecData);
    const newClose = new5SecData[4]; // Latest close price

    // Animate the current price smoothly to the new price
    animateCurrentPrice(currentPrice, newClose); // No explicit duration for gradual animation

    // Aggregate to 1-minute candle if 12 5-second data points are collected
    if (tempData.length === 12) {
        aggregateTo1Minute();
    }
}

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
        chart.updateOptions({
            annotations: {
                yaxis: [{
                    y: animatedPrice,
                    label: {
                        text: `: ${animatedPrice.toFixed(3)}`
                    }
                }]
            }
        });

        if (now - startTime < duration) {
            requestAnimationFrame(updateFrame);
        } else {
            currentPrice = endPrice; // Update the current price to the final value
        }
    }

    updateFrame();
}

// Create the chart initially
createChart();

// Update the chart every 5 seconds
setInterval(updateChart, 5000);

let socketio = io();
socketio.on("message", (e) => {
    console.log(e);
    let point = {
        x: new Date().getTime(),
        open: parseFloat(e.open),
        high: parseFloat(e.high),
        low: parseFloat(e.low),
        close: parseFloat(e.close)
    }
    console.log(point);
});
