<script>
  import FxChart from "./FxChart.svelte";

  const {data} = $props();
  console.log(data.stockData);
  console.log("+page.js");
</script>

<h1> 
  Lobby
</h1>

<FxChart stockData={data.stockData}/>
