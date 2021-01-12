from rest_framework import serializers
from .models import User, USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH

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
		try:
			receive_emails = self.validated_data["receive_emails"]
		except KeyError:
			receive_emails = False
		
		user = User(
			username=self.validated_data["username"],
			email=self.validated_data["email"],
			receive_emails=receive_emails,
			)

		for char in self.validated_data["username"]:
			if not(char.isalpha()) and not(char.isdigit()) and char != "_" and char != "-":
				raise serializers.ValidationError({"detail": "Username contains invalid characters."})

		user.set_password(self.validated_data["password"])
		user.save()

		return user

class ChangeEmailSerializer(serializers.Serializer):
	new_email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, write_only=True, required=True)
	password = serializers.CharField(max_length=PASSWORD_MAX_LENGTH, write_only=True, required=True)

	def validate(self, data):
		user = self.context['request'].user
		new_email = data["new_email"]
		password = data["password"]

		if not user.check_password(password):
			raise serializers.ValidationError({'password': ("Invalid password.")})

		if user.email == new_email:
			raise serializers.ValidationError({'new_email': ("New email cannot be the same as your current email.")})

		if User.objects.filter(email=new_email):
			raise serializers.ValidationError({'new_email': ("That email is already in use.")})

		return data

	def save(self):
		user = self.context['request'].user
		new_email = self.validated_data['new_email']

		user.email = new_email
		user.save()

		return user

class ChangeUsernameSerializer(serializers.Serializer):
	new_username = serializers.CharField(max_length=USERNAME_MAX_LENGTH, write_only=True, required=True)
	password = serializers.CharField(max_length=PASSWORD_MAX_LENGTH, write_only=True, required=True)

	def validate(self, data):
		user = self.context['request'].user
		new_username = data["new_username"]
		password = data["password"]

		if not user.check_password(password):
			raise serializers.ValidationError({'password': ("Invalid password.")})

		if user.username == new_username:
			raise serializers.ValidationError({'new_username': ("New username cannot be the same as your current username.")})

		if User.objects.filter(username=new_username):
			raise serializers.ValidationError({'new_username': ("That username is already in use.")})

		return data

	def save(self):
		user = self.context['request'].user
		new_username = self.validated_data['new_username']

		user.username = new_username
		user.save()

		return user

class ChangePasswordSerializer(serializers.Serializer):
	new_password = serializers.CharField(max_length=PASSWORD_MAX_LENGTH, write_only=True, required=True)
	old_password = serializers.CharField(max_length=PASSWORD_MAX_LENGTH, write_only=True, required=True)

	def validate(self, data):
		user = self.context['request'].user
		new_password = data["new_password"]
		old_password = data["old_password"]

		if not user.check_password(old_password):
			raise serializers.ValidationError({'old_password': ("Invalid old password.")})

		if user.check_password(new_password):
			raise serializers.ValidationError({'new_password': ("New password cannot be the same as your current password.")})

		return data

	def save(self):
		user = self.context['request'].user
		new_password = self.validated_data['new_password']

		user.set_password(new_password)
		user.save()

		return user
