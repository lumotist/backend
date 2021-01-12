**Currently deployed at:** [api-lumotist.herokuapp.com](https://api-lumotist.herokuapp.com)

# API Endpoints
## Account Endpoints
	/account/register
	/account/login
	/account/logout
	/account/user
	/account/delete
	/account/change_email
	/account/change_username
	/account/change_password

### Account field restrictions

**username**

Max length: `20`

Valid characters: Letters, numbers, `_` and `-`

**email**

Max length: `256`

**password**

Max length: `128`

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

Optionally you can provie a boolean field `receive_emails` if the user wants to receive email news, updates etc. Not providing it will by default set it to `False`.

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

If all the fields are valid, but the username contains invalid characters you will get this response:

	{
	    "detail": "Username contains invalid characters."
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

### User **(auth token required)**
Performing a GET request to `/account/user` with the users token in the **headers** will return the data for that user.

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
	        "created": "09-01-2021",
	        "receive_emails": false
	    }
	}

To see example error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).

### Delete **(auth token required)**
Performing a DELETE request to `/account/delete` with the users token in the **headers** will delete that user and the auth token.

Example DELETE request **(headers)**:

	{
	    "Authorization": "Token 2427f839b8a07d89147375921f75444094d38c05"
	}

Example successful response:

	{
	    "success": true
	}

To see example error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).

### Change Email **(auth token required)**
Performing a PUT request to `/account/change_email` with the users `password` and `new_email` will change the users email.

Example PUT request:

	{
	    "new_email": "test2@test.com",
	    "password": "test"
	}

Example successful response:

	{
	    "success": true
	}

Example error responses:

	{
	    "success": false,
	    "detail": ERROR_DETAIL
	}

ERROR_DETAIL can be the following:

	"Missing fields."
	"Ensure the new email has no more than 256 characters."
	"Invalid password."
	"New email cannot be the same as your current email."
	"That email is already in use."

To see example auth token error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).

### Change Username **(auth token required)**
Performing a PUT request to `/account/change_username` with the users `password` and `new_username` will change the users username.

Example PUT request:

	{
	    "new_username": "test2",
	    "password": "test"
	}

Example successful response:

	{
	    "success": true
	}

Example error responses:

	{
	    "success": false,
	    "detail": ERROR_DETAIL
	}

ERROR_DETAIL can be the following:

	"Missing fields."
	"Username contains invalid characters."
	"Ensure the new email has no more than 256 characters."
	"Invalid password."
	"New email cannot be the same as your current email."
	"That username is already in use."

To see example auth token error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).

### Change Password **(auth token required)**
Performing a PUT request to `/account/change_password` with the users `old_password` and `new_password` will change the users password.

Example PUT request:

	{
	    "old_password": "test",
	    "new_password": "test2"
	}

Example successful response:

	{
	    "success": true
	}

Example error responses:

	{
	    "success": false,
	    "detail": ERROR_DETAIL
	}

ERROR_DETAIL can be the following:

	"Missing fields."
	"Ensure the new password has no more than 128 characters."
	"Invalid old password."
	"New password cannot be the same as your current password."

To see example auth token error responses take a look at [Permissions](https://github.com/lumotist/backend#permissions).
