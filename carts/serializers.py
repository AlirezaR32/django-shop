from rest_framework import serializers

class AddProductToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.FloatField(default = 1)
