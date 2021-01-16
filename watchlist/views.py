from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Watchlist
from .serializers import (
	WatchlistSerializer
	)

@api_view(["GET"])
def watchlist(request, id):
	data = {}
	data["success"] = True
	data["data"] = WatchlistSerializer(Watchlist.objects.filter(id=id).first()).data

	return Response(data)
