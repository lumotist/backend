from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User
from .models import (
	USERNAME_MAX_LENGTH,
	USERNAME_MIN_LENGTH,
	EMAIL_MAX_LENGTH,
	EMAIL_MIN_LENGTH,
	PASSWORD_MIN_LENGTH,
	PASSWORD_MAX_LENGTH
	)

USERNAME_FIELD = serializers.CharField(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH, write_only=True, required=True)
EMAIL_FIELD = serializers.EmailField(min_length=EMAIL_MIN_LENGTH, max_length=EMAIL_MAX_LENGTH, write_only=True, required=True)
PASSWORD_FIELD = serializers.CharField(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH, write_only=True, required=True)
RECEIVE_EMAILS_FIELD = serializers.BooleanField(write_only=True, required=False)

USERNAME_FIELD_NOT_REQUIRED = serializers.CharField(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH, write_only=True, required=False)
EMAIL_FIELD_NOT_REQUIRED = serializers.EmailField(min_length=EMAIL_MIN_LENGTH, max_length=EMAIL_MAX_LENGTH, write_only=True, required=False)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username", "email", "created", "receive_emails"]

class RegistrationSerializer(serializers.Serializer):
	username = USERNAME_FIELD
	email = EMAIL_FIELD
	password = PASSWORD_FIELD
	receive_emails = RECEIVE_EMAILS_FIELD
	
	def validate(self, data):
		username = data["username"]
		email = data["email"]

		for char in username:
			if not(char.isalpha()) and not(char.isdigit()) and (char != "_") and (char != "-"):
				raise serializers.ValidationError({'username': ("Username should only contain letters, numbers, underscores ('_') and dashes ('-').")})

		if User.objects.filter(username=username):
			raise serializers.ValidationError({'username': ("That username is already in use.")})

		if User.objects.filter(email=email):
			raise serializers.ValidationError({'email': ("That email is already in use.")})

		return data

	def save(self):
		user = User(
			username=self.validated_data['username'],
			email=self.validated_data['email'],
			receive_emails=self.validated_data['receive_emails']
			)

		user.set_password(self.validated_data["password"])
		user.save()

		return user

class LoginSerializer(serializers.Serializer):
	username = USERNAME_FIELD_NOT_REQUIRED
	email = EMAIL_FIELD_NOT_REQUIRED
	password = PASSWORD_FIELD
	
	def validate(self, data):
		try:
			username = data["username"]
			self.provided_username = True
		except KeyError:
			self.provided_username = False

		try:
			email = data["email"]
			self.provided_email = True
		except KeyError:
			self.provided_email = False

		password = data["password"]

		if self.provided_username:
			for char in username:
				if not(char.isalpha()) and not(char.isdigit()) and (char != "_") and (char != "-"):
					raise serializers.ValidationError({'anon_field': ("Unable to log in with provided credentials.")})

			self.user = User.objects.filter(username=username).first()

			if not self.user:
				raise serializers.ValidationError({'anon_field': ("Unable to log in with provided credentials.")})

			if not self.user.check_password(password):
				raise serializers.ValidationError({'anon_field': ("Unable to log in with provided credentials.")})

		elif self.provided_email:
			self.user = User.objects.filter(email=email).first()

			if not self.user:
				raise serializers.ValidationError({'anon_field': ("Unable to log in with provided credentials.")})

			if not self.user.check_password(password):
				raise serializers.ValidationError({'anon_field': ("Unable to log in with provided credentials.")})

		else:
			raise serializers.ValidationError({'username': ("This field is required.")})

		return data

	def get_token(self):
		token = Token.objects.filter(user=self.user).first()
		if token:
			return token.key
		else:
			return Token.objects.create(user=self.user).key

class DeleteSerializer(serializers.Serializer):
	password = PASSWORD_FIELD

	def validate(self, data):
		user = self.context['request'].user
		password = data["password"]

		if not user.check_password(password):
			raise serializers.ValidationError({'password': ("Invalid password.")})

		return data

	def delete(self):
		user = self.context['request'].user

		user.auth_token.delete()
		user.delete()

class ChangeEmailSerializer(serializers.Serializer):
	new_email = EMAIL_FIELD
	password = PASSWORD_FIELD

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
	new_username = USERNAME_FIELD
	password = PASSWORD_FIELD

	def validate(self, data):
		user = self.context['request'].user
		new_username = data["new_username"]
		password = data["password"]

		for char in new_username:
			if not(char.isalpha()) and not(char.isdigit()) and (char != "_") and (char != "-"):
				raise serializers.ValidationError({'new_username': ("New username should only contain letters, numbers, underscores ('_') and dashes ('-').")})

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
	new_password = PASSWORD_FIELD
	old_password = PASSWORD_FIELD

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
