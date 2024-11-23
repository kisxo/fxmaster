<script>
  import Highcharts, { chart } from 'highcharts/highstock';
  import PriceIndicator from 'highcharts/modules/price-indicator';
  PriceIndicator(Highcharts);
  import Accessibility from 'highcharts/modules/accessibility';
  Accessibility(Highcharts);
  import { StockChart } from '@highcharts/svelte';

  let { stockData } = $props();
  console.log(stockData);

  let options = {
    title: {
        text: 'EURO / USD'
    },
    series: [{
      type: 'area',
      data: stockData,
      fillColor: {
        linearGradient: {
          x1: 0,
          y1: 0,
          x2: 0,
          y2: 1
        },
        stops: [
          [0, Highcharts.getOptions().colors[0]],
          [
            1,
            Highcharts.color(
                Highcharts.getOptions().colors[0]
            ).setOpacity(0).get('rgba')
        ]
        ]
      },
      threshold: null,
    }],
  }

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

      CustomStockChart.series[0].addPoint(newPoint);

  };

  chatSocket.onclose = function(e) {
      console.error('Chat socket closed unexpectedly');
  };

  // Create the chart when the component mounts
  let CustomStockChart;
  $effect(() => {
    CustomStockChart = Highcharts.stockChart('container', options);
  });

</script>


<div id="container" style="height: 400px; min-width: 310px"></div>

<style>
  /* your styles go here */
</style>
