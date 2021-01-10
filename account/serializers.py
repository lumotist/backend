from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username", "email", "created"]

class RegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["username", "email", "password"]
		extra_kwargs = {"password": {"write_only": True}}

	def save(self):
		user = User(
			username=self.validated_data["username"],
			email=self.validated_data["email"],
			)

		user.set_password(self.validated_data["password"])
		user.save()

		return user
