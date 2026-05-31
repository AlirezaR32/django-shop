from django.db import models
from django.conf import settings


# Create your models here.
class Order(models.Model):
    OrderStatus = ( 
        ("PENDING" : "PENDING"),
       ( "PROCESSING" : "PROCESSING"),
       ( "COMPLETED" : "COMPLETED" ),
       ( "CANCELLED" : "CANCELLED"),
       ( "FAILED" : "FAILED"),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="orders",on_delete=models.CASCADE)
    total_amount = models.CharField(max_length=32)
    status = models.CharField(max_length=1,choices =OrderStatus,default = "PENDING")
    orderd_at = models.DateTimeField(null = True,blank = True)


class OrderItem(models.Model):
    order = models.ForeignKey("Order",related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey("products.models.Product",on_delete=models.CASCADE)
    #it can be float too. (like 1.5 kg)
    quantity = models.DecimalField(max_digits=12,decimal_places=3)
    added_at = models.DateTimeField(auto_now_add = True)


