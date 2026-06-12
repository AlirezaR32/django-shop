import random
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,AddressSerializer
from .models import Address
from .services import set_new_primary_address_for_user,is_user_doesnt_have_any_addresses

User = get_user_model()

class RegisterUserView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        if User.objects.filter(username = username).exists():
            return Response({"detail" : "user with this username already registered"},
                            status = 400)
        user = User.objects.create_user(username=username,
                                 password = password)
 
        return Response({"detail" : "user been registerd successfully."},
                         status = 200)

#/users/addresses
class AddressListView(APIView):
    def get(self,request):
        addresses = Address.objects.filter(user = request.user)
        serializer = AddressSerializer(addresses,many = True)

        return Response(serializer.data,
                        status = 200)
    def post(self,request):
        serializer = AddressSerializer(data = request.data,
                                       context = {"user" : request.user}) 
        serializer.is_valid(raise_exception=True)
        if is_user_doesnt_have_any_addresses(request.user):
            serializer.save(user = request.user,
                            is_default = True) 
        else:
            serializer.save(user = request.user)
 

        return Response({"detail" : "address been added succesfully"},
                        status = 200)

class AddressDetailView(APIView):
    def get(self,request,address_id):
        address = get_object_or_404(Address,pk=address_id)
        serializer = AddressSerializer(address)
        return Response(serializer.data,
                        status = 200)

    def patch(self,request,address_id):
        address = get_object_or_404(Address,pk=address_id)
        serializer = AddressSerializer(address,data = request.data,partial = True)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["is_default"] == True:
            set_new_primary_address_for_user(user = request.user,address=address)
        
        serializer.save()
        return Response({"detaill" : "address been changed successfully"},
                        status = 200)
