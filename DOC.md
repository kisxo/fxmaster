# limit logged in user to only access data they created

  -Use filter_backends and pass a custom class as an argument which should be in file named filters.py.
  
  -As we can access django request object in that class for each request
  
# Solve stateless authentication problem in seperate frontend design(kinda)

  -Use allauth headless for all basic auth features and user related data manipulation
  
  -Allauth login api is used to retrive user data while JWT login api is used get JWT token to use in api authentication. To use rest framework JWT token for authentication, add JWT token in request header as `Authenticate: Bearer xxxxxxxxxTokenxxxxxxxxxx`
  
  -Set default authentication class to rest framework JWT authenticator

# Start svelte-kit frontend as a SPA which can be hosted by nginx  

  -Install static adapter using `npm i @sveltejs/adapter-static` and edit the svelte.config.js file to use this adapter

  -Create +layout.js file if not present in {root}/routes/ folder and set ssr and prerender value to false. If prerender is not present index.html file does not generate

# Solve 404/403 error in SPA client side routing. Caused when page is refreshed or other route like '/foo/bar' is directly accessed instead of '/'

  -In nginx configuration file use `location / { ...... try_files $uri $uri/ /index.html }` instead of `location / { ...... index index.html }` as it catches any route after the '/' and forwards it to client side router in index.html. Now if any non valid route is accessed the client side router will be responsible for handing 404/403 errors and nginx does not gets involve.
