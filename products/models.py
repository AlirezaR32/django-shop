from django.db import models
from django.utils import timezone
from .services import get_last_img_number_for_product,get_final_price

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=128)
    short_desc = models.CharField(max_length=256)
    desc = models.TextField()
    price = models.CharField(max_length=15)
    #a number between o to 1.
    off_percent = models.DecimalField(max_digits = 3,
                                      decimal_places = 2,
                                      default = 0)
    category = models.ForeignKey("Category",on_delete=models.SET_NULL)
    #a number between 0 to 5.
    review_avg_point = models.DecimalField(max_digits=3,
                                           decimal_places=2,
                                           default = 0)
    #it value has been placed after saving the product and applying off percent to price.
    final_price = models.CharField(null = True,blank = True) 
    stock_qunatity = models.PositiveIntegerField(default = 0)
    is_available = models.BooleanField(default = True)
    brand = models.ForeignKey("Brand",on_delete=models.PROTECT)
    review_count = models.PositiveSmallIntegerField(default = 0)
    view_count = models.PositiveIntegerField(default = 0)
    sell_count = models.PositiveSmallIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default=True)




    def save(self,*args,**kwargs):
        self.final_price = get_final_price(int(self.price),float(self.off_percent))
        super().save(*args,**kwargs)


    def __str__(self):
        return self.title





class Category(models.Model):
    parent = models.ForeignKey("self",on_delete=models.PROTECT)
    name = models.CharField(max_length=64)

class Brand(models.Model):
    name = models.CharField(max_length=128)
    logo = models.URLField()

class Image(models.Model):
    product = models.ForeignKey("Product",on_delete=models.CASCADE,related_name="images")
    image = models.ImageField()
    img_number = models.PositiveSmallIntegerField(null = True,blank = True)


    def save(self,*args,**kwargs):
        last_img_number = get_last_img_number_for_product(self.product)
        self.img_number = last_img_number + 1
        super().save(*args,**kwargs)


class OffCode(models.Model):
    code = models.CharField(max_length=64)
    off_percent = models.DecimalField(decimal_places=2,max_digits=3) 
    exipred_at = models.DateTimeField()

    @property
    def is_active(self):
        #it expired at must be in some time before now.
        return self.exipred_at > timezone.now()
