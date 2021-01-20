from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .models import Watchlist
from .serializers import (
	CreateSerializer,
	WatchlistSerializer
	)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create(request):
	serializer = CreateSerializer(data=request.data, context={'request': request})
	data = {}
	if serializer.is_valid():
		watchlist = serializer.save()
		data["success"] = True
		data["id"] = watchlist.id
	else:
		data["success"] = False
		data["errors"] = serializer.errors

	if data["success"]:
		return Response(data)
	else:
		return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def watchlist(request, id):
	data = {}
	try:
		watchlist = Watchlist.objects.get(id=id)
	except ObjectDoesNotExist:
		data["success"] = False
		data["error"] = "This watchlist does not exist or it might have been deleted."
		return Response(data, status=status.HTTP_400_BAD_REQUEST)

	if watchlist.public:
		watchlist.views += 1
		watchlist.save()
		data["success"] = True
		data["data"] = WatchlistSerializer(watchlist).data

	else:
		data["success"] = False
		data["error"] = "This watchlist is not public."

	if data["success"]:
		return Response(data)
	else:
		return Response(data, status=status.HTTP_400_BAD_REQUEST)
