<script>
    import Cookie from "js-cookie";
    let orderDuration = $state(1);
    let orderAmount = $state(10);


    $effect(() => {
        if(orderDuration > 5) {orderDuration = 5}
        if(orderDuration < 1) {orderDuration = 1}
    })

    $effect(() => {
        if(orderAmount > 10000) {orderAmount = 10000}
        if(orderAmount < 10) {orderAmount = 10}
    })


    async function placeOrder (side) {
        console.log("ggggggg")

        let orderData = {
            "duration": orderDuration,
            "side": side,
            "amount": orderAmount,
        }

        try {
            console.log("inside")


            let res = await fetch("http://localhost:8000/fx/orders/", {
                method: "POST",
                credentials: "include",
                body: JSON.stringify(orderData),
                headers: {
                    "X-CSRFToken": Cookie.get("csrftoken"),
                    "Content-Type": "application/json"
                }
            })

            console.log(res)
        } catch (error) {
            
        }
        
    }
</script>


<button  class="p-4 bg-green-700">Order Kro</button>

<div class="order-menu-container bg-[#f8f9fa] w-full p-3 ">
    <h3>Fixed Time Trading</h3>
    <div class="flex flex-row justify-between w-full my-3">
            <div class="flex order-input-container justify-end ">
                <button type="button" id="decrement-time-input" >-</button>
                <input type="number" bind:value={orderDuration} placeholder="&#9202; 1-5 Minute" min="1" max="5">
                <!-- <label for="time-input">Minute</label> -->
                <button type="button" id="increment-time-input">+</button>
            </div>
            <div class="flex order-input-container justify-start ">
                <button type="button" id="decrement-amount-input" >-</button>
                <input type="number" bind:value={orderAmount} placeholder="&#8377; 10-10000" min="10" max="10000">
                <button type="button" id="increment-amount-input" >+</button>
            </div>
        
    </div>
    <div class="flex flex-row w-full justify-between text-white font-bold">
        <button on:click={placeOrder("DOWN")} class="order-button bg-[#dc3545]">
            <span>Down</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-down" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1" />
            </svg>
        </button>

        <button on:click={placeOrder("UP")} class="order-button bg-[#198754]">
            <span>Up</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5" />
            </svg>
        </button>
    </div>
</div>


<style>
    .order-input-container{
        width: 48%;
        display: flex;
        justify-content: space-between;

        & > * {
            background-color: #eeeef2;
            border-radius: .3rem;
            padding: .8rem 0 .8rem 0;
        }

        & > button{
            width: 20%;
        }

        & > input{
            width: 58%;
            outline: none;
            border: none;
        }
    }

    input{
        text-align: center;
    }

    .order-button{
        width: 48%;
        padding: 1rem 0 1rem 0;
        border-radius: .3rem;
        display: flex;
        justify-content: center;
        align-content: center;
    }

    svg{
        height: auto;
    }
</style>