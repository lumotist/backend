from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from .models import USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH

@api_view(["POST"])
def register(request):
	serializer = RegistrationSerializer(data=request.data)
	data = {}
	if serializer.is_valid():
		user = serializer.save()
		data["success"] = True
		data["token"] = Token.objects.get(user=user).key
	else:
		data["success"] = False
		data["errors"] = serializer.errors

	return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
	data = {}
	request.user.auth_token.delete()
	data["success"] = True

	return Response(data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user(request):
	data = {}
	data["success"] = True
	data["data"] = UserSerializer(request.user).data

	return Response(data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete(request):
	data = {}
	request.user.auth_token.delete()
	request.user.delete()
	data["success"] = True

	return Response(data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_email(request):
	data = {}
	try:
		password = request.data["password"]
		new_email = request.data["new_email"]
	except MultiValueDictKeyError:
		data["success"] = False
		data["detail"] = "Missing fields."
		return Response(data)

	if len(new_email) > EMAIL_MAX_LENGTH:
		data["success"] = False
		data["detail"] = f"Ensure the new email has no more than {EMAIL_MAX_LENGTH} characters."

	elif not request.user.check_password(password):
		data["success"] = False
		data["detail"] = "Invalid password."

	elif new_email == request.user.email:
		data["success"] = False
		data["detail"] = "New email cannot be the same as your current email."

	else:
		try:
			request.user.email = new_email
			request.user.save()
			data["success"] = True
		except IntegrityError:
			data["success"] = False
			data["detail"] = "That email is already in use."

	return Response(data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_username(request):
	data = {}
	try:
		password = request.data["password"]
		new_username = request.data["new_username"]
	except MultiValueDictKeyError:
		data["success"] = False
		data["detail"] = "Missing fields."
		return Response(data)

	for char in new_username:
		if not(char.isalpha()) and not(char.isdigit()) and char != "_" and char != "-":
			data["success"] = False
			data["detail"] = "Username contains invalid characters."
			return Response(data)

	if len(new_username) > USERNAME_MAX_LENGTH:
		data["success"] = False
		data["detail"] = f"Ensure the new username has no more than {USERNAME_MAX_LENGTH} characters."

	elif not request.user.check_password(password):
		data["success"] = False
		data["detail"] = "Invalid password."

	elif new_username == request.user.username:
		data["success"] = False
		data["detail"] = "New username cannot be the same as your current username."

	else:
		try:
			request.user.username = new_username
			request.user.save()
			data["success"] = True
		except IntegrityError:
			data["success"] = False
			data["detail"] = "That username is already in use."

	return Response(data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
	data = {}
	try:
		old_password = request.data["old_password"]
		new_password = request.data["new_password"]
	except MultiValueDictKeyError:
		data["success"] = False
		data["detail"] = "Missing fields."
		return Response(data)

	if len(new_password) > PASSWORD_MAX_LENGTH:
		data["success"] = False
		data["detail"] = f"Ensure the new password has no more than {PASSWORD_MAX_LENGTH} characters."

	elif not request.user.check_password(old_password):
		data["success"] = False
		data["detail"] = "Invalid old password."

	elif request.user.check_password(new_password):
		data["success"] = False
		data["detail"] = "New password cannot be the same as your current password."

	else:
		request.user.set_password(new_password)
		request.user.save()
		data["success"] = True

	return Response(data)
