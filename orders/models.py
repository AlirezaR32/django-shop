from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.
class Order(models.Model):
    OrderStatus = ( 
       ( "PROCESSING" , "PROCESSING"), #جاری
       ( "COMPLETED" , "COMPLETED" ), #تحویل vشده
       ( "CANCELLED" , "CANCELLED"), #لغوشده 
       ("RETURNED" , "RETURNED") #مرحوع شده
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="orders",on_delete=models.CASCADE)
    total_amount = models.CharField(max_length=32)
    status = models.CharField(max_length=16,choices =OrderStatus,default = "PROCESSING")
    ordered_at = models.DateTimeField(auto_now_add = True,null = True,blank = True)
    cancelled_at = models.DateTimeField(null = True,blank = True)
    completed_at = models.DateTimeField(null = True,blank=True)
    returned_at = models.DateTimeField(null = True,blank = True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    #it can be float too. (like 1.5 kg)
    quantity = models.DecimalField(max_digits=12,decimal_places=3)
    added_at = models.DateTimeField(auto_now_add = True)


