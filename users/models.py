from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .validators import validate_phone_number
from .managers import UserManager



class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True,validators=[validate_phone_number])
    name = models.CharField(max_length=32,unique = True,db_index = True)
    email = models.EmailField(null = True,blank= True,unique=True)
    last_login = models.DateTimeField(auto_now_add = True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add = True)

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return f"User : self.username"
   