import random
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer,AddressSerializer
from .models import Address
from .services import set_new_default_address_for_user,is_user_doesnt_have_any_addresses
from .permissions import IsOwner

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
 
        return Response({"detail" : "user been registered successfully."},
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
        print(is_user_doesnt_have_any_addresses(request.user))
        if is_user_doesnt_have_any_addresses(request.user):
            serializer.save(user = request.user,
                            is_default = True) 
        else:
            serializer.save(user = request.user)
 

        return Response({"detail" : "address been added succesfully"},
                        status = 200)

class AddressDetailView(APIView):
    permission_classes = [IsOwner,]
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
            set_new_default_address_for_user(user = request.user,address=address)
        
        serializer.save()
        return Response({"detaill" : "address been changed successfully"},
                        status = 200)
    
    def delete(self,request,address_id):
        address = get_object_or_404(Address,pk=address_id)
        #if this address is not the only address and it's default.
        #we must set a new default address.
        is_default = address.is_default
        address.delete()
        if is_default:
            set_new_default_address_for_user(user = request.user)
        
        return Response({"detail" : "address been deleted successfully"},
                        status = 400)
