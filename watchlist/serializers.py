from rest_framework import serializers
from .models import Watchlist
from account.models import User
from .models import (
	WATCHLIST_NAME_MIN_LENGTH,
	WATCHLIST_NAME_MAX_LENGTH
	)

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
