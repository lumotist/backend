from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AnimeSerializer
from .models import Anime

@api_view(['GET'])
def entry(request, pk):
	try:
		queried_anime = Anime.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({"Error": "Invalid anime id."})

	serializer = AnimeSerializer(queried_anime, many=False)
	return Response(serializer.data)

@api_view(['GET'])
def random(request):
	random_anime = Anime.objects.order_by("?").first()
	serializer = AnimeSerializer(random_anime, many=False)
	return Response(serializer.data)
