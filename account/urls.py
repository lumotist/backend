from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name="account_register"),
    path('login', views.login, name="account_login"),
    path('logout', views.logout, name="account_logout"),
    path('user', views.user, name="account_user"),
    path('delete', views.delete, name="account_delete"),
    path('change_email', views.change_email, name="account_change_email"),
    path('change_username', views.change_username, name="account_change_username"),
    path('change_password', views.change_password, name="account_change_password"),
]
