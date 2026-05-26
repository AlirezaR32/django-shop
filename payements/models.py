from django.db import models
# Create your models here.
class Payment(models.Model):
    PaymentMethod = (
        ("bank" , "bank"),
        ("wallet" , "wallet")
    )
    PaymentStatus = (
        ('PENDING',"PENDING"),
        ("COMPLETED","COMPLETED"),
        ("FAILED","FAILED"),
        ("REFUNEDED","REFUNDED")
    )

    order = models.ForeignKey("orders.models.Order",related_name="payements",on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=16,
                                      choices = PaymentMethod)
    transaction_id = models.CharField(max_length=64)
    amount = models.CharField(max_length=32)
    status = models.CharField(max_length=16,
                              choices =PaymentStatus) 
    created_at = models.DateTimeField(auto_now_add = True)
    paid_at = models.DateTimeField(null = True,blank = True)


class ShipmentMethod(models.Model):
    name = models.CharField(max_length=64)
    cost = models.CharField(max_length=32)

class Shipment(models.Model):
    ShipmentStatus = (
            ("NOT_SHIPPED" :  "NOT_SHIPPED"),
            ("SHIPPED" : "SHIPPED"),
            ("DELIVERED" : "DELIVERED"),
            ("RETURNED" : "RETURNED"),
    )
    order = models.ForeignKey("orders.models.Order",related_name="shipments_for_order",on_delete= models.PROTECT) 
    amount = models.CharField(max_length=32)
    shipping_address = models.ForeignKey("users.models.Address",related_name = "shipments_for_address",on_delete=models.PROTECT) 
    tracking_number = models.CharField(max_length=32,null = True,blank = True) 
    status = models.CharField(max_length=16,choices=ShipmentStatus) 
    shipped_at = models.DateTimeField(null = True,blank = True) 
    delivered_at = models.DateTimeField(null = True,blank = True) 
    estimated_delieverd_at = models.DateField(null = True,blank = True)