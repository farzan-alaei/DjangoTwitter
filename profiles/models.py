from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Profile(models.Model):
    """
    Profile model for storing user profile information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"
