from rest_framework import serializers
from .models import Cart,CartItem
from products.serializers import ProductListSerializer

class AddProductToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.FloatField(default = 1)

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(many = True)
    class Meta:
        model = CartItem 
        fields = ["product","quantity","added_at"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True)
    class Meta:
        model = Cart
        fields = ["items"]

class ChangeQuantityForCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

class ApplyOffCodeSerializer(serializers.Serializer):
    code = serializers.CharField()