# API Endpoints
## Account Endpoints
	/account/register
	/account/login
	/account/logout
	/account/logoutall

### Register
Performing a POST request with the new users data will register that user, and return a auth token.
Example POST request:

	{
	    "username": "test",
	    "email": "test@test.com",
	    "password": "test"
	}

Example successful response:

	{
	    "user": {
	        "id": 18,
	        "username": "test",
	        "email": "test@test.com"
	    },
	    "token": "22c1455447b5ee0310cab3f194e3f5559d06f95ec512df15f3751cd58c514d4f"
	}

Example error response:

	{
	    "username": [
	        "A user with that username already exists."
	    ]
	}

### Login
Performing a POST request with the users data will return a auth token.
Example POST request:

	{
	    "username": "test",
	    "password": "test"
	}

Example successful response:

	{
	    "expiry": "2021-01-07T03:46:41.006710Z",
	    "token": "9f8bdef7e4d3f886e41979f2a09a191e33c95c1fb97aa72e094ecf94405e9809"
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
	    "Authorization": "Token c00a11c6fe08ed0e6a8e957214ea9fa7a70374f05dc9d8e9bd29987f4ec73a80"
	}

If the token is valid there will be no response.

Example error response:

	{
	    "detail": "Invalid token."
	}

### Logoutall
Performing a POST request with one of the users token in the **headers** will delete all the auth tokens for that user.
Example POST request **(headers)**:

	{
	    "Authorization": "Token 57ad0a6d4e422ff2b57ada2e5a810688220f7db7332759c7b98972de82bf3341"
	}

If the token is valid there will be no response.

Example error response:

	{
	    "detail": "Invalid token."
	}

### Permissions
Whenever using a endpoint that needs authentication, add the auth token in the **headers**.

	{
	    "Authorization": "Token 57ad0a6d4e422ff2b57ada2e5a810688220f7db7332759c7b98972de82bf3341"
	}

**Important:** Do not have the the auth token in the headers for endpoints that don't require it.

## Anime Endpoints
	/anime/entry/<id>
	/anime/random

### Anime Entry
Performing a GET request to:

	/anime/entry/<id>

will respond with the data for that specific anime entry.

Example request:

	/anime/entry/18562?format=json

Example response:

	{
	    "id": 18562,
	    "title": "Tokyo Ghoul",
	    "source": "https://anidb.net/anime/10401",
	    "anime_type": "TV",
	    "num_episodes": 12,
	    "status": "Finished",
	    "year": 2014,
	    "picture": "https://cdn.myanimelist.net/images/anime/5/64449.jpg",
	    "tags": [
	        "Action",
	        "Crime",
	        "Dark fantasy",
	        "Drama",
	        "Gore",
	        "Horror",
	        "Human experimentation",
	        "Male protagonist",
	        "Mystery",
	        "Police",
	        "Psychological",
	        "Seinen",
	        "Supernatural",
	        "Survival",
	        "Tragedy",
	        "Violence"
	    ]
	}

### Anime Random
Performing a GET request to:

	/anime/random

will respond with the data for a random anime entry.

Example request:

	/anime/random?format=json

Example response:

	{
	    "id": 12839,
	    "title": "Nisekoi",
	    "source": "https://anidb.net/anime/9903",
	    "anime_type": "TV",
	    "num_episodes": 20,
	    "status": "Finished",
	    "year": 2014,
	    "picture": "https://cdn.myanimelist.net/images/anime/13/75587.jpg",
	    "tags": [
	        "Comedy",
	        "Female protagonist",
	        "Gangs",
	        "Harem",
	        "Love polygon",
	        "Love triangle",
	        "Mafia",
	        "Male protagonist",
	        "Romance",
	        "Romantic comedy",
	        "School",
	        "School life",
	        "Shounen",
	        "Slice of life"
	    ]
	}
