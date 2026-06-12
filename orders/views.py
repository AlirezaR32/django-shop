from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from carts.services import get_or_create_cart_for_user
from orders.services import get_erros_for_stock_availablity_of_cart_items,get_total_amount_of_cart,create_order_from_cart,is_cart_empty
from orders.models import Order

from .serializers import OrderDetailSerializer,OrderListSerializer 

#filter by status too.
#sort by recieve time too.
class OrderListView(APIView):
    def get(self,request):
        orders = Order.objects.filter(user = request.user)
        if request.query_params.get("status"):
            orders = orders.filter(status = request.query_params.get("status"))

        serializer = OrderListSerializer(orders,many = True)
        return Response(serializer.data,
                        status = 200)

class OrderDetailView(APIView):
    def get(self,request,order_id):
        order = get_object_or_404(Order,pk = order_id)
        serilaizer = OrderDetailSerializer(order)
        return Response(serilaizer.data,
                        status = 200)

class CancellOrderView(APIView):
    def patch(self,request,order_id):
        order = get_object_or_404(Order,pk = order_id) 
        if order.status == "CANCELLED":
            return Response({"detail" : "order has been cancelled before"},
                            status = 200)
        order.status = "CANCELLED"
        order.save(update_fields=["status",])
        return Response({"detail" : "order has been successfully cancelled"},
                        status = 200)

class CheckOutView(APIView):
    def post(self,request):
        cart = get_or_create_cart_for_user(request.user)
        
        stock_validation_errors = get_erros_for_stock_availablity_of_cart_items(cart = cart)

        if stock_validation_errors:
            return Response({"detail" : "stock_quantity_error",
                             "errors" : stock_validation_errors},
                            status = 400)
        
        if is_cart_empty(cart):
            return Response({"detail" : "the cart is empty"},
                            status = 400) 
        total_amount = get_total_amount_of_cart(cart = cart)
        #after an order placed from an cart.
        #the old cart must become inactive.
        order = create_order_from_cart(total_amount=total_amount,
                                cart = cart)
        cart.is_active = False
        cart.save(update_fields=["is_active",]) 

        return Response({"order_id" : order.pk,
                         "total_amount" : total_amount})