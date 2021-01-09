**Currently deployed at:** [api-lumotist.herokuapp.com](https://api-lumotist.herokuapp.com])

# API Endpoints
## Account Endpoints
	/account/register
	/account/login
	/account/logout
	/account/profile
	/account/delete
	/account/get_pictures
	/acount/set_picture

### Permissions
Whenever using a endpoint that needs authentication, add the auth token in the **headers**.

	{
	    "Authorization": "Token 2427f839b8a07d89147375921f75444094d38c05"
	}

Endpoints that require a auth token will have **(auth token required)** in their documentation.

**Important:** Do not have the the auth token in the headers for endpoints that don't require it.

Example error response for invalid token:

	{
	    "detail": "Invalid token."
	}

Example error response for missing auth token:

	{
	    "detail": "Authentication credentials were not provided."
	}

### Register
Performing a POST request to `/account/register` with the new users `username`, `email` and `password` will register that user, and return a auth token.
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
Performing a POST request to `/account/login` with the users `username` and `password` will return a auth token.

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

### Logout **(auth token required)**
Performing a POST request to `/account/logout` with the users token in the **headers** will delete that auth token.

Example POST request **(headers)**:

	{
	    "Authorization": "Token 2427f839b8a07d89147375921f75444094d38c05"
	}

Example successful response:

	{
	    "success": true
	}

To see example error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).

### Profile **(auth token required)**
Performing a GET request to `/account/profile` with the users token in the **headers** will return the data for that user.

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

To see example error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).

### Delete **(auth token required)**
Performing a POST request to `/account/delete` with the users token in the **headers** will delete that user and the auth token.

Example POST request **(headers)**:

	{
	    "Authorization": "Token 2427f839b8a07d89147375921f75444094d38c05"
	}

Example successful response:

	{
	    "success": true
	}

To see example error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).

## Get Pictures **(auth token required)**
Performing a GET request to `/account/get_pictures` with the users token in the **headers** will return all the pictures that the user can set as their profile picture.

Example GET request **(headers)**:

	{
	    "Authorization": "Token 2427f839b8a07d89147375921f75444094d38c05"
	}

Successful response will return the `profile_pictures` dictionary in [profile_pictures.py](https://github.com/lumotist/backend/blob/master/account/profile_pictures.py).

To see example error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).

### Set Picture
Performing a POST request to `/account/set_picture` with the picture `id` from `/account/get_pictures` will update the users profile picture.

**Note:** After registration, by default the users profile picture is set to `default_profile_picture` in [profile_pictures.py](https://github.com/lumotist/backend/blob/master/account/profile_pictures.py).

Example POST request:

	{
	    "id": 6
	}

Example successful response:

	{
	    "success": true
	}

Example error response:

	{
	    "success": false,
	    "error": "Invalid picture id."
	}

To see example auth error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).
