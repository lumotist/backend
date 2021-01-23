from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Watchlist
from account.models import User
from .models import (
	WATCHLIST_NAME_MIN_LENGTH,
	WATCHLIST_NAME_MAX_LENGTH,
	ANIME_ID_MIN_SIZE,
	ANIME_ID_MAX_SIZE
	)

ID_FIELD = serializers.IntegerField(write_only=True, required=True)
NAME_FIELD = serializers.CharField(min_length=WATCHLIST_NAME_MIN_LENGTH, max_length=WATCHLIST_NAME_MAX_LENGTH, write_only=True, required=True)
PUBLIC_FIELD = serializers.BooleanField(write_only=True, required=True)
ANIMES_FIELD = serializers.CharField(write_only=True, required=True)
ANIME_FIELD = serializers.IntegerField(min_value=ANIME_ID_MIN_SIZE, max_value=ANIME_ID_MAX_SIZE, write_only=True, required=True)

class WatchlistSerializer(serializers.ModelSerializer):
	# Author will be set to the username of the author
	author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
     )

	class Meta:
		model = Watchlist
		fields = ["id", "name", "public", "animes", "author", "created", "updated", "views"]

class WatchlistMinimalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Watchlist
		fields = ["id", "name", "created", "updated", "views"]

class CreateSerializer(serializers.Serializer):
	name = NAME_FIELD

	def validate(self, data):
		user = self.context['request'].user
		name = data["name"]

		try:
			user.watchlists.get(name=name)
			raise serializers.ValidationError({'name': ("You already have a watchlist with that name.")})
		except ObjectDoesNotExist:
			pass

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
		watchlist = Watchlist(
			name=self.validated_data["name"],
			author=self.context['request'].user
			)
		
		watchlist.save()

		return watchlist

class DeleteSerializer(serializers.Serializer):
	id = ID_FIELD

	def validate(self, data):
		user = self.context['request'].user
		id = data["id"]

		try:
			self.watchlist = Watchlist.objects.get(id=id)
		except ObjectDoesNotExist:
			raise serializers.ValidationError({'id': ("Invalid watchlist id.")})

		if self.watchlist.author != user:
			raise serializers.ValidationError({'user': ("The auth user is not the author of the watchlist.")})

		return data

	def delete(self):
		self.watchlist.delete()

class UpdateNameSerializer(serializers.Serializer):
	id = ID_FIELD
	new_name = NAME_FIELD

	def validate(self, data):
		user = self.context['request'].user
		id = data["id"]
		new_name = data["new_name"]

		try:
			self.watchlist = Watchlist.objects.get(id=id)
		except ObjectDoesNotExist:
			raise serializers.ValidationError({'id': ("Invalid watchlist id.")})

		if self.watchlist.author != user:
			raise serializers.ValidationError({'user': ("The auth user is not the author of the watchlist.")})

		if self.watchlist.name == new_name:
			raise serializers.ValidationError({'new_name': ("The new name cannot be the same as the current name.")})

		try:
			user.watchlists.get(name=new_name)
			raise serializers.ValidationError({'new_name': ("You already have a watchlist with that name.")})
		except ObjectDoesNotExist:
			pass

		return data

	def save(self):
		self.watchlist.name = self.validated_data['new_name']
		self.watchlist.save()

		return self.watchlist

class UpdatePublicSerializer(serializers.Serializer):
	id = ID_FIELD
	new_public = PUBLIC_FIELD

	def validate(self, data):
		user = self.context['request'].user
		id = data["id"]
		new_public = data["new_public"]

		try:
			self.watchlist = Watchlist.objects.get(id=id)
		except ObjectDoesNotExist:
			raise serializers.ValidationError({'id': ("Invalid watchlist id.")})

		if self.watchlist.author != user:
			raise serializers.ValidationError({'user': ("The auth user is not the author of the watchlist.")})

		if self.watchlist.public == new_public:
			raise serializers.ValidationError({'new_public': (f"This watchlists public status is already set to {new_public}")})

		return data

	def save(self):
		self.watchlist.public = self.validated_data['new_public']
		self.watchlist.save()

		return self.watchlist

class UpdateAnimesSerializer(serializers.Serializer):
	id = ID_FIELD
	new_animes = ANIMES_FIELD

	def validate(self, data):
		user = self.context['request'].user
		id = data["id"]
		new_animes = data["new_animes"]

		try:
			self.watchlist = Watchlist.objects.get(id=id)
		except ObjectDoesNotExist:
			raise serializers.ValidationError({'id': ("Invalid watchlist id.")})

		if self.watchlist.author != user:
			raise serializers.ValidationError({'user': ("The auth user is not the author of the watchlist.")})

		# This part is a little sloppy, maybe try to improve it later
		# Check if the new animes is a valid array
		if ("[" not in new_animes) or ("]" not in new_animes):
			raise serializers.ValidationError({'new_animes': ("A valid array is required.")})
		elif (new_animes[0] != "[") or (new_animes[len(new_animes) - 1] != "]"):
			raise serializers.ValidationError({'new_animes': ("A valid array is required.")})

		# Convert it into an array
		self.validated_new_animes = new_animes.strip("[").strip("]").split(",")

		# Check if each element is a valid integer, if so convert them into a integer
		for index, element in enumerate(self.validated_new_animes):
			try:
				int_element = int(element)
			except ValueError:
				raise serializers.ValidationError({'new_animes': ("The elements in the array should be valid integers.")})

			# Check if the integer is out of range
			if int_element > ANIME_ID_MAX_SIZE:
				raise serializers.ValidationError({'new_animes': ("A integer in the array is out of range.")})

			self.validated_new_animes[index] = int_element

		# Check if the array contains more than one of the same anime
		for anime in self.validated_new_animes:
			if self.validated_new_animes.count(anime) > 1:
				raise serializers.ValidationError({'new_animes': ("The watchlist contains more than one of the same anime.")})

		# Check the length of the anime
		if len(self.validated_new_animes) > 500:
			raise serializers.ValidationError({'new_animes': ("Maximum number of 500 animes reached.")})

		if self.watchlist.animes == self.validated_new_animes:
			raise serializers.ValidationError({'new_animes': ("The new animes cannot be the same as the current animes.")})

		return data

	def save(self):
		self.watchlist.animes = self.validated_new_animes
		self.watchlist.save()

		return self.watchlist

class AddAnimeSerializer(serializers.Serializer):
	id = ID_FIELD
	anime = ANIME_FIELD

	def validate(self, data):
		user = self.context['request'].user
		id = data["id"]
		anime = data["anime"]

		try:
			self.watchlist = Watchlist.objects.get(id=id)
		except ObjectDoesNotExist:
			raise serializers.ValidationError({'id': ("Invalid watchlist id.")})

		if self.watchlist.author != user:
			raise serializers.ValidationError({'user': ("The auth user is not the author of the watchlist.")})

		if anime in self.watchlist.animes:
			raise serializers.ValidationError({'anime': (f"This anime is already in the watchlist.")})

		return data

	def save(self):
		self.watchlist.animes.append(self.validated_data['anime'])
		self.watchlist.save()

		return self.watchlist

class RemoveAnimeSerializer(serializers.Serializer):
	id = ID_FIELD
	anime = ANIME_FIELD

	def validate(self, data):
		user = self.context['request'].user
		id = data["id"]
		anime = data["anime"]

		try:
			self.watchlist = Watchlist.objects.get(id=id)
		except ObjectDoesNotExist:
			raise serializers.ValidationError({'id': ("Invalid watchlist id.")})

		if self.watchlist.author != user:
			raise serializers.ValidationError({'user': ("The auth user is not the author of the watchlist.")})

		if anime not in self.watchlist.animes:
			raise serializers.ValidationError({'anime': (f"This anime is already not in the watchlist.")})

		return data

	def save(self):
		self.watchlist.animes.remove(self.validated_data['anime'])
		self.watchlist.save()

		return self.watchlist

class CheckAnimeSerializer(serializers.Serializer):
	id = ID_FIELD
	anime = ANIME_FIELD

	def validate(self, data):
		user = self.context['request'].user
		id = data["id"]
		anime = data["anime"]

		try:
			self.watchlist = Watchlist.objects.get(id=id)
		except ObjectDoesNotExist:
			raise serializers.ValidationError({'id': ("Invalid watchlist id.")})

		if self.watchlist.author != user:
			raise serializers.ValidationError({'user': ("The auth user is not the author of the watchlist.")})

		return data

	def check_anime(self):
		if self.validated_data['anime'] in self.watchlist.animes:
			return True
		else:
			return False
