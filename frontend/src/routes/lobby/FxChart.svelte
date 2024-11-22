<script>
  import Highcharts, { chart } from 'highcharts/highstock';
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
    series: [{
        type: 'line',
    }]
  };

  options.series[0].data = [
    [
        1317888000000,
        100.5101,
    ],
];

  const chatSocket = new WebSocket(
    'ws://localhost:8000/ws/fxupdatechannel/fxupdateroom/'
);

chatSocket.onmessage = function(e) {
    const response = JSON.parse(e.data);
    console.log(response);


    let newPoint = [
        response.data.period,
        response.data.price,
    ]

};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// Create the chart when the component mounts
let CustomStockChart;

import { onMount } from 'svelte';
onMount(() => {
        CustomStockChart = Highcharts.stockChart('container', options);
    }
);

</script>

<div id="container" style="height: 400px; min-width: 310px"></div>

<style>
  /* your styles go here */
</style>
