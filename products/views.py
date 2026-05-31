from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter,SearchFilter 
from rest_framework.pagination import PageNumberPagination  
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer  
from .services import ProductFilter

#/products?
class ProductListView(APIView):
    #in default order.
    def get(self,request):
        product_filter = ProductFilter(request)
        products = product_filter.run()
        serializer = ProductSerializer(products,
                                       many = True)
        
        return Response(serializer.data,
                        status = 200)
    



class ProductDetailView(APIView):
    def get(self,request,product_id):
        product = get_object_or_404(Product,pk = product_id)
        Serializer = ProductSerializer(product)
        product.view_count += 1
        return Response(Serializer.data,
                        status = 200)





