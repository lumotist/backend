from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.watchlist, name="watchlist_watchlist"),
]
