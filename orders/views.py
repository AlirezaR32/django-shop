from rest_framework.views import APIView
from rest_framework.response import Response

from carts.services import get_or_create_cart_for_user
from orders.services import get_erros_for_stock_availablity_of_cart_items,get_total_amount_of_cart,create_order_from_cart
from orders.models import Order

class CheckOutView(APIView):
    def post(self,request):
        cart = get_or_create_cart_for_user(request.user)
        
        stock_validation_errors = get_erros_for_stock_availablity_of_cart_items(cart = cart)

        if stock_validation_errors:
            return Response({"detail" : "stock_quantity_error",
                             "errors" : stock_validation_errors,}
                            status = 400)
        

        total_amount = get_total_amount_of_cart(cart = cart)

        order = create_order_from_cart(total_amount=total_amount,
                                cart = cart)
        
        return Response({"order_id" : order.pk,
                         total_amount : total_amount})