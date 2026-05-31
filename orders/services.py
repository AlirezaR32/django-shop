from carts.models import Cart
from orders.models import Order,OrderItem

def get_erros_for_stock_availablity_of_cart_items(cart : Cart) -> dict:
    validation_errors = {}

    for item in cart.items.select_related("product"):
        if item.quantity > item.product.stock_quantity:
            validation_errors[f"item.product"] = {"user_quantity" : item.quantity,
                                                  "stock_quantity" : item.product.stock_quantity} 

    return validation_errors


def get_total_amount_of_cart(cart : Cart):
    total_amount = 0 
    for item in cart.items.select_related("product"):
        total_amount += item.product.final_price
    if cart.off_code and cart.off_code.is_active:
        total_amount -= cart.off_code.off_percent * total_amount 
    return total_amount


def create_order_from_cart(cart : Cart,total_amount : int) -> Order:
    order = Order.objects.create(user = cart.user,
                                 total_amount = total_amount)

    for item in cart.items:
        OrderItem.objects.create(order = order,
                                 product = item.product,
                                 quantity = item.quantity)

    return order 