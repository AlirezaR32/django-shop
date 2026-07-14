from carts.models import Cart
from orders.models import Order,OrderItem
from products.models import Product
from django.db.models import F

def get_erros_for_stock_availablity_of_cart_items(cart : Cart) -> dict:
    validation_errors = {}

    for item in cart.items.select_related("product"):
        if item.quantity > item.product.stock_quantity:
            validation_errors[f"{item.product}"] = {"user_quantity" : item.quantity,
                                                  "stock_quantity" : item.product.stock_quantity} 

    return validation_errors


def get_total_amount_of_cart(cart : Cart):
    total_amount = 0 
    for item in cart.items.select_related("product"):
        #the final price is sth like this -> 10000.0
        total_amount += item.product.final_price
    if cart.off_code and cart.off_code.is_active:
        #i cast the off_percent from Decimal type to float to make the * valid.
        # (*) operation can't be execute between a <float> and a <decimal>.
        total_amount -= float(cart.off_code.off_percent) * total_amount 
    return total_amount


def create_order_from_cart(cart : Cart,total_amount : int) -> Order:
    order = Order.objects.create(user = cart.user,
                                 total_amount = total_amount)

    for item in cart.items.all():
        OrderItem.objects.create(order = order,
                                 product = item.product,
                                 quantity = item.quantity)

    return order 

def is_cart_empty(cart : Cart) -> bool:
    return cart.items.count() == 0


def change_stock_quantity_of_order_items_in_db(order : Order,increase : bool = False):
    if increase:
        for item in order.items.select_related("product"):
            Product.objects.filter(pk=item.product_id).update(
            stock_quantity=F("stock_quantity") + item.quantity
        )
    else :
        for item in order.items.select_related("product"):
            Product.objects.filter(pk=item.product_id).update(
            stock_quantity=F("stock_quantity") - item.quantity
        )