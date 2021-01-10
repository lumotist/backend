from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username", "email", "created", "receive_emails"]

class RegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["username", "email", "password", "receive_emails"]
		extra_kwargs = {"password": {"write_only": True}}

	def save(self):
		user = User(
			username=self.validated_data["username"],
			email=self.validated_data["email"],
			receive_emails=self.validated_data["receive_emails"],
			)

		user.set_password(self.validated_data["password"])
		user.save()

		return user
