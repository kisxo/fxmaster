<script>
  import { onMount } from 'svelte';
	import '../app.css';
	let { children } = $props();

  	import Navbar from './Navbar.svelte';
	import axios from 'axios';

	onMount(() => {
		axios.get('http://localhost:8000/csrf/',
		{withCredentials: true})
		.then(function (response) {
			console.log(response);
		})
		.catch(function (error) {
			console.log(error);
		});
	});
    
</script>

<Navbar />
{@render children()}
