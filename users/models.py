from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from .validators import validate_postal_code


class User(AbstractBaseUser):
    username = models.CharField(max_length=32)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"User : self.username"

class Address(models.Model):
    user = models.ForeignKey("user",related_name="addresses",on_delete=models.CASCADE)  
    full_address = models.CharField(null = True,blank = True,max_length=512)
    longtiude = models.PositiveIntegerField(null = True,blank = True)
    city = models.CharField(null = True,blank = True,max_length=32)
    state = models.CharField(null = True,blank = True,max_length=32)
    postal_code  = models.CharField(max_length = 10,validators=[validate_postal_code,],null = True,blank = True)
    is_default = models.BooleanField(default = True)



