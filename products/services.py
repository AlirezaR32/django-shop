from .models import Product

def get_last_img_number_for_product(product : Product):
    images = product.images.all()
    if images:
        last_img_number = images[-1].img_number 
        return last_img_number
    return 0


def get_final_price(price : int,
                    off_percent : float):
    final_price = (1 - off_percent) * price
    return final_price