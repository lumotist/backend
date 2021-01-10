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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete(request):
	data = {}
	request.user.auth_token.delete()
	request.user.delete()
	data["success"] = True

	return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_email(request):
	data = {}
	try:
		password = request.data["password"]
		new_email = request.data["new_email"]
	except:
		data["success"] = False
		data["detail"] = "Missing fields."
		return Response(data)

	if len(new_email) > 256:
		data["success"] = False
		data["detail"] = "Ensure the new email has no more than 256 characters."

	elif not request.user.check_password(password):
		data["success"] = False
		data["detail"] = "Invalid password."

	elif new_email == request.user.email:
		data["success"] = False
		data["detail"] = "New email cannot be the same as your current email."

	else:
		request.user.email = new_email
		request.user.save()
		data["success"] = True

	return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
	data = {}
	try:
		old_password = request.data["old_password"]
		new_password = request.data["new_password"]
	except:
		data["success"] = False
		data["detail"] = "Missing fields."
		return Response(data)

	if len(new_password) > 128:
		data["success"] = False
		data["detail"] = "Ensure the new password has no more than 128 characters."

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
