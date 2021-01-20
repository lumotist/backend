from django.urls import path
from . import views

urlpatterns = [
	path("create", views.create, name="watchlist_create"),
    path("<int:id>", views.watchlist, name="watchlist_watchlist"),
]
