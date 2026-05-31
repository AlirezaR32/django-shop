from users.models import User
from .models import Cart,CartItem
from products.models import Product


def get_or_create_cart_for_user(user : User):
    try :
        cart = Cart.objects.get(user = user,
                               is_active = True)
    except:
        cart = Cart.objects.create(user = user)
    
    return cart


def is_product_in_cart(product : Product,cart : Cart) -> bool:
    for item in cart.items:
        if item.product == product:
            return True
    
    return False


def is_product_available(product : Product,
                         quantity : float):
    return product.stock_qunatity >= quantity 