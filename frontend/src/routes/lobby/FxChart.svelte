<script>
  import Highcharts from 'highcharts/highstock';
  import PriceIndicator from 'highcharts/modules/price-indicator';
  PriceIndicator(Highcharts);
  import Indicators from 'highcharts/indicators/indicators-all';
  Indicators(Highcharts);
  import Accessibility from 'highcharts/modules/accessibility';
  Accessibility(Highcharts);
  import { StockChart } from '@highcharts/svelte';

  const options = {
    title: {
        text: 'EURO / USD'
    },

    xAxis: {
        overscroll: 500000,
        range: 4 * 200000,
        gridLineWidth: 1
    },

    rangeSelector: {
        buttons: [{
            type: 'minute',
            count: 15,
            text: '15m'
        }, {
            type: 'hour',
            count: 1,
            text: '1h'
        }, {
            type: 'all',
            count: 1,
            text: 'All'
        }],
        selcted: 1,
        inputEnabled: false
    },

    navigator: {
        series: {
            color: '#000000'
        }
    },

    series: [{
        type: 'candlestick',
        color: '#FF7F7F',
        upColor: '#90EE90',
        lastPrice: {
            enabled: true,
            label: {
                enabled: true,
                backgroundColor: '#FF7F7F'
            }
        }
    }]
  };

// Imitate getting point from backend
function getNewPoint(i, data) {
    const lastPoint = data[data.length - 1];

    // Add new point
    if (i === 0 || i % 10 === 0) {
        return [
            lastPoint[0] + 60000,
            lastPoint[4],
            lastPoint[4],
            lastPoint[4],
            lastPoint[4]
        ];
    }
    const updatedLastPoint = data[data.length - 1],
        newClose = Highcharts.correctFloat(
            lastPoint[4] + Highcharts.correctFloat(Math.random() - 0.5, 2),
            4
        );

    // Modify last data point
    return [
        updatedLastPoint[0],
        data[data.length - 2][4],
        newClose >= updatedLastPoint[2] ? newClose : updatedLastPoint[2],
        newClose <= updatedLastPoint[3] ? newClose : updatedLastPoint[3],
        newClose
    ];
}

// On load, start the interval that adds points
options.chart = {
    events: {
        load() {
            const chart = this,
                series = chart.series[0];

            let i = 0;

            setInterval(() => {
                const data = series.options.data,
                    newPoint = getNewPoint(i, data),
                    lastPoint = data[data.length - 1];

                // Different x-value, we need to add a new point
                if (lastPoint[0] !== newPoint[0]) {
                    series.addPoint(newPoint);
                } else {
                // Existing point, update it
                    series.options.data[data.length - 1] = newPoint;

                    series.setData(data);
                }
                i++;
            }, 100);
        }
    }
};



options.series[0].data = [
    [
        1317888000000,
        372.5101,
        375,
        372.2,
        372.52
    ],
    [
        1317888060000,
        372.4,
        373,
        372.01,
        372.16
    ],
    [
        1317888120000,
        372.16,
        372.4,
        371.39,
        371.62
    ],
    [
        1317888180000,
        371.62,
        372.16,
        371.55,
        371.75
    ],
    [
        1317888240000,
        371.75,
        372.4,
        371.57,
        372
    ],
    [
        1317888300000,
        372,
        372.3,
        371.8,
        372.24
    ],
    [
        1317888360000,
        372.22,
        372.45,
        372.22,
        372.3
    ],
    [
        1317888420000,
        372.3,
        373.25,
        372.3,
        373.15
    ],
    [
        1317888480000,
        373.01,
        373.5,
        373,
        373.24
    ],
    [
        1317888540000,
        373.36,
        373.88,
        373.19,
        373.88
    ],
    [
        1317888600000,
        373.8,
        374.34,
        373.75,
        374.29
    ],
    [
        1317888660000,
        374.29,
        374.43,
        374,
        374.01
    ],
    [
        1317888720000,
        374.05,
        374.35,
        373.76,
        374.35
    ],
    [
        1317888780000,
        374.41,
        375.24,
        374.37,
        374.9
    ],
    [
        1317888840000,
        374.83,
        375.73,
        374.81,
        374.96
    ],
    [
        1317888900000,
        374.81,
        375.4,
        374.81,
        375.25
    ],
    [
        1317888960000,
        375.2,
        375.7,
        375.14,
        375.19
    ],
    [
        1317889020000,
        375.43,
        375.43,
        374.75,
        374.76
    ],
  ];


</script>

<StockChart {options} highcharts = {Highcharts}/>

<style>
  /* your styles go here */
</style>
