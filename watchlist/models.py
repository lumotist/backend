from django.db import models
from django.contrib.postgres.fields import ArrayField
from account.models import User

WATCHLIST_NAME_MIN_LENGTH = 1
WATCHLIST_NAME_MAX_LENGTH = 64

ANIME_ID_MIN_SIZE = 0
ANIME_ID_MAX_SIZE = 2147483647

class Watchlist(models.Model):
	name = models.CharField(max_length=WATCHLIST_NAME_MAX_LENGTH)
	public = models.BooleanField(default=False)
	animes = ArrayField(models.IntegerField(), size=500, null=True, default=[])
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	views = models.IntegerField(default=0)

	def __str__(self):
		return self.name
