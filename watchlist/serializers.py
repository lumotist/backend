from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Watchlist
from account.models import User
from .models import (
	WATCHLIST_NAME_MIN_LENGTH,
	WATCHLIST_NAME_MAX_LENGTH
	)

ID_FIELD = serializers.IntegerField()
NAME_FIELD = serializers.CharField(min_length=WATCHLIST_NAME_MIN_LENGTH, max_length=WATCHLIST_NAME_MAX_LENGTH, write_only=True, required=True)

class WatchlistSerializer(serializers.ModelSerializer):
	author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
     )

	class Meta:
		model = Watchlist
		fields = ["id", "name", "public", "animes", "author", "created", "updated", "views"]


class CreateSerializer(serializers.Serializer):
	name = NAME_FIELD

	def save(self):
		watchlist = Watchlist(
			name=self.validated_data["name"],
			author=self.context['request'].user
			)
		
		watchlist.save()

		return watchlist

class UpdateNameSerializer(serializers.Serializer):
	id = ID_FIELD
	name = NAME_FIELD

	def validate(self, data):
		user = self.context['request'].user
		id = data["id"]
		name = data["name"]

		try:
			self.watchlist = Watchlist.objects.get(id=id)
		except ObjectDoesNotExist:
			raise serializers.ValidationError({'id': ("Invalid watchlist id.")})

		if self.watchlist.author != user:
			raise serializers.ValidationError({'user': ("The auth user is not the author of the watchlist.")})

		if self.watchlist.name == name:
			raise serializers.ValidationError({'name': ("The new name cannot be the same as the current name.")})

		return data

	def save(self):
		self.watchlist.name = self.validated_data['name']
		self.watchlist.save()

		return self.watchlist
