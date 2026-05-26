from django.db import models
from .services import get_last_img_number_for_product,get_final_price

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=128)
    short_desc = models.CharField(max_length=256)
    desc = models.TextField()
    price = models.CharField(max_length=15)
    #a number between o to 1.
    off_percent = models.DecimalField(max_digits = 3,
                                      decimal_places = 2)
    category = models.ForeignKey("Category",on_delete=models.SET_NULL)
    #a number between 0 to 5.
    review_avg_point = models.DecimalField(max_digits=3,
                                           decimal_places=2)
    #it value has been placed after saving the product and applying off percent to price.
    final_price = models.CharField(null = True,blank = True) 
    stock_qunatity = models.PositiveIntegerField(default = 0)
    brand = models.ForeignKey("Brand",on_delete=models.PROTECT)
    review_count = models.PositiveSmallIntegerField(default = 0)
    view_count = models.PositiveIntegerField(default = 0)
    sell_count = models.PositiveSmallIntegerField(default = 0)
    #in kg
    weight = models.DecimalField(max_digits=6,
                                 decimal_places=3)
    dimensions = models.CharField(max_length=16)
    #in days.
    warranty_period = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)




    def save(self,*args,**kwargs):
        self.final_price = get_final_price(int(self.price),float(self.off_percent))
        super().save(*args,**kwargs)






class Attirbute(models.Model):
    name = models.CharField(max_length=64)
    is_filter = models.BooleanField(default = False)


class ProductAttribute(models.Model):
    product = models.ForeignKey("Product",related_name="attributes",on_delete=models.CASCADE)
    Attirbute = models.ForeignKey("Attribute",on_delete=models.PROTECT)
    value = models.CharField(max_length=64)


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



class Review:
    ...