# API Endpoints
## Account Endpoints
	/account/register
	/account/login
	/account/logout
	/account/profile
	/account/delete

### Register
Performing a POST request with the new users `username`, `email` and `password` will register that user, and return a auth token.
Example POST request:

	{
	    "username": "test",
	    "email": "test@test.com",
	    "password": "test"
	}

Example successful response:

	{
	    "success": true,
	    "token": "b68e6599d205430b37c6d3bde5b174ca3af1f385"
	}

Example error response:

	{
	    "success": false,
	    "errors": {
	        "username": [
	            "user with this username already exists."
	        ],
	        "email": [
	            "user with this email already exists."
	        ]
	    }
	}

### Login
Performing a POST request with the users `username` and `password` will return a auth token.

**Note:** If there is already a auth token generated for that user, it will return that auth token.

Example POST request:

	{
	    "username": "test",
	    "password": "test"
	}

Example successful response:

	{
	    "token": "b68e6599d205430b37c6d3bde5b174ca3af1f385"
	}

Example error response:

	{
	    "non_field_errors": [
	        "Unable to log in with provided credentials."
	    ]
	}

### Logout
Performing a POST request with the users token in the **headers** will delete that auth token.
Example POST request **(headers)**:

	{
	    "Authorization": "Token 2427f839b8a07d89147375921f75444094d38c05"
	}

Example successful response:

	{
	    "success": true
	}

Example error response:

	{
	    "detail": "Invalid token."
	}

### Profile
Performing a GET request with the users token in the **headers** will return the data for that user.
Example GET request **(headers)**:

	{
	    "Authorization": "Token 2427f839b8a07d89147375921f75444094d38c05"
	}

Example successful response:

	{
	    "success": true,
	    "data": {
	        "id": 2,
	        "username": "test1",
	        "email": "test@test.com1",
	        "created": "09-01-2021"
	    }
	}

Example error response:

	{
	    "detail": "Invalid token."
	}

### Delete
Performing a POST request with the users token in the **headers** will delete that user and the auth token.
Example POST request **(headers)**:

	{
	    "Authorization": "Token 2427f839b8a07d89147375921f75444094d38c05"
	}

Example successful response:

	{
	    "success": true,
	}

Example error response:

	{
	    "detail": "Invalid token."
	}

### Permissions
Whenever using a endpoint that needs authentication, add the auth token in the **headers**.

	{
	    "Authorization": "Token 2427f839b8a07d89147375921f75444094d38c05"
	}

**Important:** Do not have the the auth token in the headers for endpoints that don't require it.
