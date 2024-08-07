from django.db import models

# Create your models here.


class Profile(models.Model):
    """
    TwitterProfile model
    """

    user = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="twitter_profile",
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"
