# limit logged in user to only access data they created

  -Use filter_backends and pass a custom class as an argument which should be in file named filters.py.
  
  -As we can access django request object in that class for each request
  
# Solve stateless authentication problem in seperate frontend design(kinda)

  -Use allauth headless for all basic auth features and user related data manipulation
  
  -Allauth login api is used to retrive user data while JWT login api is used get JWT token to use in api authentication. To use rest framework JWT token for authentication, add JWT token in request header as `Authenticate: Bearer xxxxxxxxxTokenxxxxxxxxxx`
  
  -Set default authentication class to rest framework JWT authenticator