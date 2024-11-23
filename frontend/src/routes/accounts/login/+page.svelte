<script>
    import axios from "axios";
    let name = '', email = '', password = '';

    async function submit (){
        axios.post('http://localhost:8000/_allauth/browser/v1/auth/login', {
            email,
            password
        })
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
    }
</script>

<h2>register</h2>

<form on:submit|preventDefault={submit}>
    <input bind:value={email} type="email" name="email" id="">
    <input bind:value={password} type="password" name="password" id="">
    <button type="submit">Submit</button>
</form>