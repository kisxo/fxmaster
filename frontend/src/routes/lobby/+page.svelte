<script>
  import { goto } from "$app/navigation";
  import FxChart from "./FxChart.svelte";
  import OrderMenu from "./OrderMenu.svelte";

  const {data} = $props();
  console.log(data.stockData);
  console.log("+page.js");
  console.log(data)
  if(!data.isAllowed){
    goto("/accounts/login")
  }
</script>

<FxChart stockData={data.stockData}/>
<OrderMenu />
