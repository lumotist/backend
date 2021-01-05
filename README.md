# API Endpoints
	/anime/entry/<id>
	/anime/random

**Note:** To format the response in json format add `?format=json` to the end of the url.
Example:

	/anime/random?format=json

# Anime Entry
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

# Anime Random
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
