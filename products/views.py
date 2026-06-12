from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductDetailSerializer,ProductListSerializer  
from .services import ProductFilter
from .pagination import StandardPagination

#/products?
class ProductListView(APIView):
    #in default order.
    permission_classes = (AllowAny,)
    def get(self,request):
        product_filter = ProductFilter(request)
        products = product_filter.run()
        paginator = StandardPagination() 
        page = paginator.paginate_queryset(products,request)
        serializer = ProductListSerializer(page , many = True)
        return paginator.get_paginated_response(serializer.data)
       


#products/<product_id>
class ProductDetailView(APIView):
    permission_classes = (AllowAny,)
    def get(self,request,product_id):
        product = get_object_or_404(Product,pk = product_id,is_active = True)
        Serializer = ProductDetailSerializer(product)
        product.view_count += 1
        product.save(update_fields = ["view_count",])
        return Response(Serializer.data,
                        status = 200)





