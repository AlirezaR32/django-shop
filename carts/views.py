from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .serializers import AddProductToCartSerializer,ChangeQuantityForCartItemSerializer
from .services import get_or_create_cart_for_user,is_product_in_cart,is_product_available
from .models import CartItem
from .serializers import CartSerializer 

from products.models import Product,OffCode



#in this view user get's its own cart.
#cart/
class GetCartView(APIView):
    def get(self,request):
        cart = get_or_create_cart_for_user(user = request.user)
        serializer = CartSerializer(cart)

        return Response(serializer.data,
                        status = 200)

#post cart/items
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

        quantity = serializer.validated_data["quantity"]
        is_available = is_product_available(prodcut = product,quantity = quantity) 

        if not is_available:
            return Response({"detail" : "product with this quantity isn't availabe in stock"},
                            status = 400)

        CartItem.objects.create(cart = user_cart,
                                product = product,
                                quantity = serializer.validated_data["quantity"]) 
        
        return Response({"detail" : "the item has been added to user's cart"},
                        status = 200)

#patch cart/items/<item_id>
class ChangeQuantityForCartItemView(APIView):
    def patch(self,request,item_id):
        serializer = ChangeQuantityForCartItemSerializer(data = request.data)
        cart_item = get_object_or_404(CartItem,pk = item_id) 
        if not cart_item.cart.is_active :
            return Response({"detail" : "this cart isn't active to update."},
                            status = 400)

        quantity = serializer.validated_data["quantity"]
        is_available = is_product_available(product=cart_item.product,
                             quantity=quantity)
        
        if not is_available:
            return Response({"detail" : "product with this quantity isn't availabe in stock"},
                                status = 400)

        cart_item.quantity = quantity
        cart_item.save(update_fields=["quantity"])
        return Response({"detail" : "quantity for this item has been changed"},
                        status = 200)

    def delete(self,request,cartitem_id):
        cartitem = get_object_or_404(CartItem,pk = cartitem_id)
        cartitem.delete()
        return Response({"detail" : "cartitem been deleted successfully"},
                        status = 200)

#cart/apply-off-code
class ApplyOffCodeView(APIView):
    def post(self,request):
        serializer = CartSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        off_code = get_object_or_404(OffCode,code = serializer.validated_data["code"])

        cart = get_or_create_cart_for_user(user = request.user)

        if not cart.off_code.is_active:
            return Response({"detail" : "off code is expired"},
                            status = 200)

        cart.off_code = off_code
        cart.save(update_fields=["off_code",])

        return Response({"detail" : "off code been applied successfully"},
                        status = 200)
