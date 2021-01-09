from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token

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
def profile(request):
	data = {}
	data["success"] = True
	data["data"] = UserSerializer(request.user).data

	return Response(data)
