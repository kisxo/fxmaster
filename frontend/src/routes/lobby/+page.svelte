<script>
  import { goto } from "$app/navigation";
  import FxChart from "./FxChart.svelte";

  const {data} = $props();
  console.log(data.stockData);
  console.log("+page.js");
  console.log(data)
  if(!data.isAllowed){
    goto("/accounts/login")
  }
</script>

<h1> 
  Lobby
</h1>

<FxChart stockData={data.stockData}/>
