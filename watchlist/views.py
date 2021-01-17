from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .models import Watchlist
from .serializers import (
	WatchlistSerializer
	)

@api_view(["GET"])
def watchlist(request, id):
	data = {}
	try:
		watchlist = Watchlist.objects.get(id=id)
		watchlist.views += 1
		watchlist.save()
		data["success"] = True
		data["data"] = WatchlistSerializer(watchlist).data
	except ObjectDoesNotExist:
		data["success"] = False
		data["error"] = "This watchlist does not exist or maybe it was deleted."

	if data["success"]:
		return Response(data)
	else:
		return Response(data, status=status.HTTP_400_BAD_REQUEST)
