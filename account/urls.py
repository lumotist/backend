from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register', views.register, name="account_register"),
    path('login', obtain_auth_token, name="account_login"),
    path('logout', views.logout, name="account_logout"),
    path('profile', views.profile, name="account_profile"),
    path('delete', views.delete, name="account_delete"),
]
