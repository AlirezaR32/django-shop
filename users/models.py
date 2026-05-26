from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager



class User(AbstractBaseUser):
    username = models.CharField(max_length=32)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"User : self.username"
   