from django.db import models
from products.models import Product,OffCode
from django.conf import settings 
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="carts",on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default = True)
    off_code = models.ForeignKey(OffCode,on_delete=models.SET_NULL,null = True,blank = True)


class CartItem(models.Model):
    cart = models.ForeignKey("Cart",related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    #it can be float too. (like 1.5 kg)
    quantity = models.DecimalField(max_digits=12,decimal_places=3)
    added_at = models.DateTimeField(auto_now_add = True)


