<script>
  import { slide } from 'svelte/transition';
  import { page } from '$app/stores';

  let isDropdownOpen = false // default to close

  const handleDropdownClick = () => {
    isDropdownOpen = !isDropdownOpen; // togle state
  }

  const handleDropdownFocusLoss = ({ relatedTarget, currentTarget }) => {
    if (relatedTarget instanceof HTMLElement && currentTarget.contains(relatedTarget)) return
    // check if the new focus target doesn't present in the dropdown tree (exclude ul\li padding area because relatedTarget, in this case, will be null) 
    isDropdownOpen = false;
  }

  let navLinks = [
    { name: "Lobby", path: "/lobby"},
    { name: "Profile", path: "/profile"},
    { name: "Login",  path: "/accounts/login"},
    { name: "Logout",  path: "/accounts/logout"},
  ]

  let currentPage = "Profile";

</script>

<div class="w-100 flex-col box-shadow border" on:focusout={handleDropdownFocusLoss}>
  <div class="w-100 px-3 py-2 flex flex-row justify-between">
    <a href="/" class="justify-between" aria-label="logo">
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        class="inline-block h-6 w-6" 
        viewBox="0 0 500 200" 
        fill="currentColor">
                <path d="M250 25.5V0H300L375 75L450 0H500V25L375 150L250 25.5Z" fill="#5865F2"/>
                <path d="M93 100L0 0H65L157 100L65 200H0L93 100Z" fill="#5865F2"/>
                <path d="M250 60V200H300V110L250 60Z" fill="black"/>
                <path d="M450 200H500V60L450 110V200Z" fill="black"/>
                <path d="M185 0L143 46L175 81L250 0H185Z" fill="black"/>
                <path d="M143 154L175 119L250 200H185L143 154Z" fill="black"/>
      </svg>
    </a>
    <button class="text-gray-600" on:click={handleDropdownClick}>
      {#if isDropdownOpen}
		  	<svg
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								class="inline-block h-6 w-6 stroke-current border-2 border-primary border-primary rounded">
								<title>Close Dropdown</title>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M6 18L18 6M6 6l12 12" />
							</svg>
		  	{:else}
		  	<svg
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								class="inline-block h-6 w-6 stroke-current">
								<title>Open Dropdown</title>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M4 6h16M4 12h16M4 18h16" />
				</svg>
			{/if}
    </button>
  </div>

  {#if isDropdownOpen}
    <div transition:slide class="text-xs font-bold border-t border-[#5046E5] flex flex-col text-gray-600"> 
      {#each navLinks as navLink}
          <a href="{navLink.path}" class="px-3 py-1" class:active-nav-link={$page.url.pathname === navLink.path}> {navLink.name} </a>
	    {/each}
    </div>
  {/if}

</div>

<style>
  .box-shadow {
    box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
  }

  a {
    border-left: solid 4px #ffffff;
  }

  .active-nav-link {
    border-left: solid 4px #5046E5;
    background-color: #EEF2FE;
    color: #5046E5;
  }

</style>
