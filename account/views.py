from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegistrationSerializer
from .models import User
from rest_framework.authtoken.models import Token

from .profile_pictures import profile_pictures

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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete(request):
	data = {}
	request.user.auth_token.delete()
	request.user.delete()
	data["success"] = True

	return Response(data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_pictures(request):
	return Response(profile_pictures)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_picture(request):
	user = User.objects.get(id=request.user.id)
	data = {}
	try:
		picture_id = int(request.data["id"])

		if (picture_id >= 1) and (picture_id <= 5):
			user.picture = profile_pictures["male"][picture_id - 1]["picture"]
		elif (picture_id >= 5) and (picture_id <= 10):
			user.picture = profile_pictures["female"][picture_id - 6]["picture"]
		else:
			# Any error would work
			raise ValueError
		user.save()
		data["success"] = True
	except:
		data["success"] = False
		data["error"] = "Invalid picture id."

	return Response(data)
