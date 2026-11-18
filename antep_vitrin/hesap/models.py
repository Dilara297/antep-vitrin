from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    telefon = models.CharField(max_length=20, blank=True, null=True)
    adres = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profili"