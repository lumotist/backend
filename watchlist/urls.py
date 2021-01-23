from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.watchlist, name="watchlist_watchlist"),
    path("create", views.create, name="watchlist_create"),
    path("update_name", views.update_name, name="watchlist_update_name"),
    path("update_public", views.update_public, name="watchlist_update_public"),
    path("update_animes", views.update_animes, name="watchlist_update_animes"),
    path("add_anime", views.add_anime, name="watchlist_add_anime"),
]
