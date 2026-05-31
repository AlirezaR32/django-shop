from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .serializers import AddProductToCartSerializer
from .services import get_or_create_cart_for_user,is_product_in_cart
from .models import CartItem

from products.models import Product


class AddProductToCart(APIView):
    def post(self,request):
        serializer = AddProductToCartSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product,pk = serializer.validated_data["product_id"],is_active = True)
        user_cart = get_or_create_cart_for_user(user = request.user)

        is_product_in_user_cart = is_product_in_cart(product = product,
                                                  cart = user_cart)
        
        if is_product_in_user_cart:
            return Response({"detail" : "the product is already in cart"},
                            status = 400)
        
        CartItem.objects.create(cart = user_cart,
                                product = product,
                                quantity = serializer.validated_data["quantity"]) 
        
        return Response({"detail" : "the item has been added to user's cart"},
                        status = 200)