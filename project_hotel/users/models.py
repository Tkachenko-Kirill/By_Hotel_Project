from django.db import models
from django.contrib.auth.models import User

from django_resized import ResizedImageField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=40, blank=False)
    profile_image = ResizedImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return self.username