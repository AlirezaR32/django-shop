from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Address

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 32) 
    password = serializers.CharField(max_length = 16) 

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"