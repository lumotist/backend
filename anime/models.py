from django.db import models
from django.contrib.postgres.fields import ArrayField

class Anime(models.Model):
	title = models.CharField(max_length=156)
	source = models.CharField(max_length=145)
	anime_type = models.CharField(max_length=7, db_index=True)
	num_episodes = models.IntegerField(db_index=True)
	status = models.CharField(max_length=9, db_index=True)
	year = models.IntegerField(db_index=True)
	picture = models.CharField(max_length=168)
	tags = ArrayField(models.CharField(max_length=27), db_index=True)

	def __str__(self):
		return self.title
