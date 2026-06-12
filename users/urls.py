from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from .views import RegisterUserView,AddressDetailView,AddressListView

urlpatterns = [
    path("auth/register",RegisterUserView.as_view(),name="register"),
    path("auth/token",TokenObtainPairView.as_view(),name = "get-token"),
    path("auth/token/refresh",TokenRefreshView.as_view(),name="refresh-token"),
    path("addresses",AddressListView.as_view(),name="address-list"),
    path("addresses/<address_id>",AddressDetailView.as_view(),name="address-detail"),
]