from rest_framework.permissions import BasePermission


class IsOwnerOfCartItem(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.uesr == obj.cart.user