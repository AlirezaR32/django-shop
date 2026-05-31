from .models import Product,Category,Brand
from rest_framework.request import HttpRequest 
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from typing import Optional


def get_last_img_number_for_product(product : Product):
    images = product.images.all()
    if images:
        last_img_number = images[-1].img_number 
        return last_img_number
    return 0


def get_final_price(price : int,
                    off_percent : float):
    final_price = (1 - off_percent) * price
    return final_price


class ProductFilter:
    def __init__(self,request : Request) -> None:
        self.products = Product.objects.filter(is_active = True).order_by("-created_at")
        self.query_params = request.query_params

    def sort(self):
        sort_val = self.query_params.get("sort")
        descending_sort = self.query_params.get("descending")
        order_field = None
        if sort_val:
            match sort_val:
                case "point":
                    if descending_sort:
                        order_field = "-review_avg_point"
                    else:
                        order_field = "review_avg_point"
                case "price":
                    if descending_sort:
                        order_field = "-final_price"
                    else:
                        order_field = "price"
                case "view":
                    if descending_sort:
                        order_field = "-view_count"
                    else:
                        order_field = "view_count"
                case "sell":
                    if descending_sort:
                        order_field = "-sell_count"
                    else:
                        order_field = "sell_count"

            self.products = self.products.order_by(order_field)

 

    
    def filter(self):
        category_name = self.query_params.get("category")
        has_off = self.query_params.get("has_off")
        is_available = self.query_params.get("is_available")
        brand_name = self.query_params.get("brand")

        if category_name:
            category = get_object_or_404(Category,name = category_name) 
            self.products = self.products.filter(category = category)
        if has_off:
            self.products = self.products.filter(off_percent__gt=0)
        if is_available:
            self.products = self.products.filter(is_available=True)
        if brand_name:
            brand = get_object_or_404(Brand,name = brand_name)
            self.products = self.products.filter(brand = brand)
        

    
    def search(self):
        search_text = self.query_params.get('search')
        if search_text:
            self.products = self.products.filter(title__icontains = search_text)



    def run(self):
        self.products = self.sort()
        self.products = self.filter()
        self.products = self.search()
        return self.products