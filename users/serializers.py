from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 32) 
    password = serializers.CharField(max_length = 16) 
