from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from datetime import timedelta

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=128)
    short_desc = models.CharField(max_length=256,null = True,blank = True)
    desc = models.TextField(null = True,blank = True)
    price = models.CharField(max_length=15)
    #a number between o to 1.
    off_percent = models.DecimalField(max_digits = 3,
                                      decimal_places = 2,
                                      default = 0)
    category = models.ForeignKey("Category",on_delete=models.PROTECT)
    #a number between 0 to 5.
    review_avg_point = models.DecimalField(max_digits=3,
                                           decimal_places=2,
                                           default = 0)
    #it value has been placed after saving the product and applying off percent to price.
    final_price = models.CharField(null = True,blank = True) 
    stock_quantity = models.PositiveIntegerField(default = 0)
    brand = models.ForeignKey("Brand",on_delete=models.PROTECT,null = True,blank = True)
    review_count = models.PositiveSmallIntegerField(default = 0)
    view_count = models.PositiveIntegerField(default = 0)
    sell_count = models.PositiveSmallIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default=True)

    @property
    def is_available(self):
        return self.stock_quantity > 0
    
    def get_final_price(self,price : int, off_percent : float):
     final_price = (1 - off_percent) * price 
     return final_price


    def save(self,*args,**kwargs):
        self.final_price = str(self.get_final_price(int(self.price),float(self.off_percent)))
        super().save(*args,**kwargs)


    def __str__(self):
        return self.title





class Category(models.Model):
    parent = models.ForeignKey("self",on_delete=models.PROTECT,null=True,blank=True)
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=128)
    logo = models.URLField(null = True,blank = True)

    def __str__(self) -> str:
        return self.name

class Image(models.Model):
    product = models.ForeignKey("Product",on_delete=models.CASCADE,related_name="images")
    image = models.ImageField()
    img_number = models.PositiveSmallIntegerField(null = True,blank = True)


    
    def get_last_img_number_for_product(self,product):
        images = product.images.all()
        if images:
            last_img_number = images[-1].img_number 
            return last_img_number
        return 0

    def save(self,*args,**kwargs):
        last_img_number = self.get_last_img_number_for_product(self.product)
        self.img_number = last_img_number + 1
        super().save(*args,**kwargs)
    
    def __str__(self) -> str:
        return f"image {self.img_number} for product {self.product}"


class OffCode(models.Model):
    code = models.CharField(max_length=64)
    off_percent = models.DecimalField(decimal_places=2,max_digits=3) 
    #by default every off code has a 1day duration to use.
    expire_duration = models.DurationField(default = timedelta(days=1))
    created_at = models.DateTimeField(auto_now_add = True)
    @property
    def expired_at(self):
        #it expired at must be in some time before now.
        return self.created_at + self.expire_duration

    @property 
    def is_active(self):
        return timezone.now() < self.expired_at

    def __str__(self) -> str:
        return self.code
