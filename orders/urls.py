from django.urls import path
from .views import OrderDetailView,OrderListView,CancellOrderView,CheckOutView

urlpatterns = [
    path("",OrderListView.as_view(),name="order-list"),
    path("<int:order_id>",OrderDetailView.as_view(),name="order-detail"),
    path("<int:order_id>/cancell",CancellOrderView.as_view(),name="cancell-order"),
    path("checkout",CheckOutView.as_view(),name="checkout")
]