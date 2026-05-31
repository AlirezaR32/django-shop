from .models import User,Address

def is_user_doesnt_have_any_addresses(user : User):
    addresses = user.addresses
    return len(addresses) == 0

def get_default_address_for_user(user : User):
    for address in user.addresses:
        if address.is_default :
            return address
    raise ValueError("user doesnt have any fucking default address")

def set_new_primary_address_for_user(user : User,
                                     address : Address):
    if not address.is_default: 
        user_default_address = get_default_address_for_user(user = user)
        user_default_address.is_default = False
        user_default_address.save(update_fields = ["is_default",])
        address.is_default = True
        address.save(update_fields=["is_default",])
    