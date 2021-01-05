from django.urls import path
from . import views

urlpatterns = [
    path('entry/<int:pk>', views.entry, name="anime_entry"),
    path('random', views.random, name="anime_random"),
]
