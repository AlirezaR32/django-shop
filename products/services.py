from .models import Product,Category,Brand
from django.shortcuts import get_object_or_404
from rest_framework.request import HttpRequest



class ProductFilter:
    def __init__(self,request : HttpRequest) -> None:
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
                        order_field = "final_price"
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
            if order_field:
                self.products = self.products.order_by(order_field)

 

    
    def filter(self):
        category_name = self.query_params.get("category")
        has_off = self.query_params.get("has_off")
        is_available = self.query_params.get("is_available")
        brand_name = self.query_params.get("brand")

        if category_name:
            category = get_object_or_404(Category,name__iexact = category_name) 
            self.products = self.products.filter(category = category)
        #"" is excepted too.
        #the user can send a request like this -> products/has_off&category=""
        #and has_off applied to it.
        if has_off is not None:
            self.products = self.products.filter(off_percent__gt=0)
        if is_available is not None:
            self.products = self.products.filter(stock_quantity__gt=0)
        if brand_name:
            brand = get_object_or_404(Brand,name = brand_name)
            self.products = self.products.filter(brand = brand)
        

    
    def search(self):
        search_text = self.query_params.get('search')
        if search_text:
            self.products = self.products.filter(title__icontains = search_text)



    def run(self):
        self.sort()
        self.filter()
        self.search()
        return self.products