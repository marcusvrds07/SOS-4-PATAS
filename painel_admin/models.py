from django.contrib.auth.models import User
from django.db import models

def user_profile_photo_path(instance, filename):
    return f'usuarios/{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to=user_profile_photo_path, blank=True, null=True)

    def __str__(self):
        return self.user.username