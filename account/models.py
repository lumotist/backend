from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20

EMAIL_MIN_LENGTH = 3
EMAIL_MAX_LENGTH = 256

PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 128

class User(AbstractUser):
	username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True)
	email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	receive_emails = models.BooleanField(default=False)

# Create a auth token when saving a user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
