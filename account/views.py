from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import (
	UserSerializer,
	RegistrationSerializer,
	LoginSerializer,
	DeleteSerializer,
	ChangeEmailSerializer,
	ChangeUsernameSerializer,
	ChangePasswordSerializer)

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

	if data["success"]:
		return Response(data)
	else:
		return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def login(request):
	serializer = LoginSerializer(data=request.data)
	data = {}
	if serializer.is_valid():
		data["success"] = True
		data["token"] = serializer.get_token()
	else:
		data["success"] = False
		data["errors"] = serializer.errors

	if data["success"]:
		return Response(data)
	else:
		return Response(data, status=status.HTTP_400_BAD_REQUEST)

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
	serializer = DeleteSerializer(data=request.data, context={'request': request})
	data = {}
	if serializer.is_valid():
		serializer.delete()
		data["success"] = True
	else:
		data["success"] = False
		data["errors"] = serializer.errors

	if data["success"]:
		return Response(data)
	else:
		return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_email(request):
	serializer = ChangeEmailSerializer(data=request.data, context={'request': request})
	data = {}
	if serializer.is_valid():
		serializer.save()
		data["success"] = True
	else:
		data["success"] = False
		data["errors"] = serializer.errors

	if data["success"]:
		return Response(data)
	else:
		return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_username(request):
	serializer = ChangeUsernameSerializer(data=request.data, context={'request': request})
	data = {}
	if serializer.is_valid():
		serializer.save()
		data["success"] = True
	else:
		data["success"] = False
		data["errors"] = serializer.errors

	if data["success"]:
		return Response(data)
	else:
		return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
	serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
	data = {}
	if serializer.is_valid():
		serializer.save()
		data["success"] = True
	else:
		data["success"] = False
		data["errors"] = serializer.errors

	if data["success"]:
		return Response(data)
	else:
		return Response(data, status=status.HTTP_400_BAD_REQUEST)
