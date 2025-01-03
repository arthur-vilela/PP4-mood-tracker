from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Email for notifications
    username = models.CharField(max_length=150, unique=True)  # Username for login

    def __str__(self):
        return self.username
