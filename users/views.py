import random
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

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
        User.objects.create_user(username=username,
                                 password = password)
        return Response({"detail" : "user registered successfully"}
                        ,status = 200)

class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User,username = serializer.validated_data["username"])
        if not user.check_password(serializer.validated_data["password"]):
            return Response({"detail" : "the password is incorrect"},
                            status = 400)

        token = RefreshToken.for_user(user)
        return Response({"refresh" : token,
                         "access" : token.access_token},
                         status = 200)



   