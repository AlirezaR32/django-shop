from .models import User,Address
from typing import Optional

def is_user_doesnt_have_any_addresses(user : User):
    return user.addresses.count() == 0 

def get_default_address_for_user(user : User):
    for address in user.addresses.all():
        if address.is_default :
            return address
    raise ValueError("user doesnt have any fucking default address")

def set_new_default_address_for_user(user : User,
                                     address : Optional[Address] = None):
    if address:          
        if not address.is_default: 
            user_default_address = get_default_address_for_user(user = user)
            user_default_address.is_default = False
            user_default_address.save(update_fields = ["is_default",])
            address.is_default = True
            address.save(update_fields=["is_default",])
    else:
        first_address = user.addresses.order_by("-created_at").first()
        if first_address:
            first_address.is_default = True
            first_address.save(update_fields = ["is_default",])
        