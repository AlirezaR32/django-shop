from django.urls import path
from .views import GetCartView ,ApplyOffCodeView,CartItemDetailView


urlpatterns = [
    path("cart",GetCartView.as_view(),name="get-cart"),
    path("cart/<int:item_id>",CartItemDetailView.as_view(),name="change-cart"),
    path("cart/apply-off-code",ApplyOffCodeView.as_view(),name="apply-off-code-to-cart"),
]