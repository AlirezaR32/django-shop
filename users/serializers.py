from rest_framework import serializers

from django.contrib.auth import get_user_model

from .validators import PhoneNumberValidator 

User = get_user_model()


class GetCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length = 12,validators = (PhoneNumberValidator,))

class CheckCodeSerializer(serializers.Serializer):
    phone_number =  serializers.CharField(max_length = 12,validators = (PhoneNumberValidator,)) 
    code = serializers.IntegerField()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "phone_number", "password",)
        extra_kwargs = {"password": {"write_only": True}}

    #so when you said something like user.save()
    #it triggers the createuser function.
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","password","phone_number")
        read_only_fields = ["phone_number"]
        extra_kwargs =  {"password": {"write_only": True}}

class ChangePasswordSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length = 12)
    code = serializers.IntegerField()
    new_password = serializers.CharField()