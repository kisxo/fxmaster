<script>
  import Highcharts, { chart, stockChart } from 'highcharts/highstock';
  import PriceIndicator from 'highcharts/modules/price-indicator';
  PriceIndicator(Highcharts);
  import Accessibility from 'highcharts/modules/accessibility';
  Accessibility(Highcharts);
  import { StockChart } from '@highcharts/svelte';

  let { stockData } = $props();
  console.log(stockData);

  function zoomUpdate(event) {
    setTimeout(() => {
      console.log("chart clickkkkk")
      console.log(event)
      var zoom_level = CustomStockChart.xAxis[0].getExtremes().max - CustomStockChart.xAxis[0].getExtremes().min
      console.log(zoom_level)

      if ( zoom_level < 310000)
      {
        CustomStockChart.xAxis[0].update({
          overscroll: 100 * 1000
        });
      }
      else if ( zoom_level < 910000)
      {
        CustomStockChart.xAxis[0].update({
          overscroll: 330 * 1000
        });
      }
      else if ( zoom_level < 3700000)
      {
        CustomStockChart.xAxis[0].update({
          overscroll: 1100 * 1000
        });
      }
      else
      {
        CustomStockChart.xAxis[0].update({
          overscroll: '50%'
        });
      }

    }, 250);
  }

  let options = {
    title: {
        text: 'EURO / USD'
    },
    credits: {
      enabled: false
    },
    xAxis: {
        overscroll: 100 * 1000,
    },
    rangeSelector: {
        buttons: [{
            count: 5,
            type: 'minute',
            text: '5M',
        },
        {
            count: 15,
            type: 'minute',
            text: '15M',
        },
        {
            count: 1,
            type: 'hour',
            text: '1H',
        },
        {
            type: 'all',
            text: 'Reset'
        }],
        inputEnabled: false,
        selected: 0
    },
    series: [{
      type: 'area',
      data: stockData,
      lastPrice: {
        color: '#FF7F7F',
        enabled: true,
        label: {
          enabled: true,
          backgroundColor: '#FF7F7F',
          formatter: (value) => {
              return value.toFixed(4);
          },
        }
      },
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


<div on:click={zoomUpdate} id="container" style="height: 400px; min-width: 310px"></div>

<style>
  /* your styles go here */
</style>
