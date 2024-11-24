<script>
  import { goto } from "$app/navigation";
    import Cookie from "js-cookie";
    
    async function logout() {
        console.log("logout")

        try {
            let res = await fetch('http://localhost:8000/_allauth/browser/v1/auth/session', {
                method: "DELETE",
                credentials: "include",
                headers: {
                    "X-CSRFToken": Cookie.get("csrftoken"),
                }
            })

            if(res.status === 401)
            {
                goto("/")
            }
        } catch (error) {
            
        }
      
    }
</script>

<button  on:click={logout}>Log out</button>

<style>
    button{
        background-color: aqua;
    }
</style>