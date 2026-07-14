from django.test import TestCase

# Create your tests here.
import pytest
from decimal import Decimal

from products.models import Product
from carts.models import Cart

from .models import Order, OrderItem
from .fixtures import *


# =================================================================
# OrderListView  GET /orders/
# =================================================================

@pytest.mark.django_db
class TestOrderListView:

    def test_get_requires_authentication(self, api_client):
        response = api_client.get(ORDER_LIST_URL)

        assert response.status_code in (401, 403)

    def test_get_returns_200(self, auth_client, order):
        response = auth_client.get(ORDER_LIST_URL)

        assert response.status_code == 200

    def test_get_returns_only_current_users_orders(self, auth_client, order, other_user_order):
        response = auth_client.get(ORDER_LIST_URL)
        returned_ids = [o["id"] for o in response.data]

        assert order.id in returned_ids
        assert other_user_order.id not in returned_ids

    def test_get_returns_empty_list_when_no_orders(self, auth_client):
        response = auth_client.get(ORDER_LIST_URL)

        assert response.status_code == 200
        assert response.data == []

    def test_get_filters_by_status(self, auth_client, order, completed_order):
        response = auth_client.get(ORDER_LIST_URL, {"status": "COMPLETED"})
        returned_ids = [o["id"] for o in response.data]

        assert completed_order.id in returned_ids
        assert order.id not in returned_ids


# =================================================================
# OrderDetailView  GET /orders/<id>/
# =================================================================

@pytest.mark.django_db
class TestOrderDetailView:

    def test_get_requires_authentication(self, api_client, order):
        response = api_client.get(order_detail_url(order.id))

        assert response.status_code in (401, 403)

    def test_get_owner_returns_200(self, auth_client, order):
        response = auth_client.get(order_detail_url(order.id))

        assert response.status_code == 200

    def test_get_includes_items(self, auth_client, order, order_item):
        response = auth_client.get(order_detail_url(order.id))

        assert len(response.data["items"]) == 1
        assert response.data["items"][0]["id"] == order_item.id

    def test_get_nonexistent_order_returns_404(self, auth_client):
        response = auth_client.get(order_detail_url(99999))

        assert response.status_code == 404

    def test_get_non_owner_returns_403(self, other_auth_client, order):
        response = other_auth_client.get(order_detail_url(order.id))

        assert response.status_code == 403


# =================================================================
# CancellOrderView  POST /orders/<id>/cancell/
# =================================================================

@pytest.mark.django_db
class TestCancellOrderView:

    def test_post_requires_authentication(self, api_client, order):
        response = api_client.post(cancel_order_url(order.id))

        assert response.status_code in (401, 403)

    def test_post_cancels_order_returns_200(self, auth_client, order):
        response = auth_client.post(cancel_order_url(order.id))

        assert response.status_code == 200

    def test_post_sets_status_to_cancelled(self, auth_client, order):
        auth_client.post(cancel_order_url(order.id))
        order.refresh_from_db()

        assert order.status == "CANCELLED"

    def test_post_sets_cancelled_at_timestamp(self, auth_client, order):
        auth_client.post(cancel_order_url(order.id))
        order.refresh_from_db()

        assert order.cancelled_at is not None

    def test_post_restores_stock_quantity(self, auth_client, order, product):
        OrderItem.objects.create(order=order, product=product, quantity=Decimal("3"))
        original_stock = product.stock_quantity

        auth_client.post(cancel_order_url(order.id))
        product.refresh_from_db()

        assert product.stock_quantity == original_stock + 3

    def test_post_already_cancelled_order_returns_200_with_message(self, auth_client, cancelled_order):
        response = auth_client.post(cancel_order_url(cancelled_order.id))

        assert response.status_code == 400 
        assert "can't canell this order" in response.data["detail"]

    def test_post_nonexistent_order_returns_404(self, auth_client):
        response = auth_client.post(cancel_order_url(99999))

        assert response.status_code == 404

    def test_post_non_owner_returns_403(self, other_auth_client, order):
        response = other_auth_client.post(cancel_order_url(order.id))

        assert response.status_code == 403


# =================================================================
# CheckOutView  POST /orders/checkout/
# =================================================================

@pytest.mark.django_db
class TestCheckOutView:

    def test_post_requires_authentication(self, api_client):
        response = api_client.post(CHECKOUT_URL)

        assert response.status_code in (401, 403)

    def test_post_empty_cart_returns_400(self, auth_client, cart):
        response = auth_client.post(CHECKOUT_URL)

        assert response.status_code == 400
        assert "empty" in response.data["detail"]

    def test_post_insufficient_stock_returns_400(self, auth_client, cart_with_two_understocked_items):
        response = auth_client.post(CHECKOUT_URL)

        assert response.status_code == 400
        assert response.data["detail"] == "stock_quantity_error"

    def test_post_reports_stock_errors_for_all_insufficient_items(
        self, auth_client, cart_with_two_understocked_items
    ):
        """
        Both items in this cart exceed their stock. A correct implementation
        should report a validation error per affected product.
        """
        response = auth_client.post(CHECKOUT_URL)

        assert len(response.data["errors"]) == 2

    def test_post_creates_order_from_cart(self, auth_client, user, cart_with_item):
        response = auth_client.post(CHECKOUT_URL)

        assert response.status_code == 200
        assert Order.objects.filter(user=user).exists()

    def test_post_creates_order_items_matching_cart_items(self, auth_client, cart_with_item, product):
        response = auth_client.post(CHECKOUT_URL)
        order = Order.objects.get(pk=response.data["order_id"])

        assert order.items.filter(product=product).exists()

    def test_post_deactivates_old_cart(self, auth_client, cart_with_item):
        auth_client.post(CHECKOUT_URL)
        cart_with_item.refresh_from_db()

        assert cart_with_item.is_active is False

    def test_post_decreases_stock_quantity(self, auth_client, cart_with_item, product):
        original_stock = product.stock_quantity

        auth_client.post(CHECKOUT_URL)
        product.refresh_from_db()

        assert product.stock_quantity == original_stock - 2

    def test_post_response_contains_order_id_and_total_amount(self, auth_client, cart_with_item):
        response = auth_client.post(CHECKOUT_URL)

        assert "order_id" in response.data
        assert "total_amount" in response.data

    def test_post_applies_off_code_discount_to_total_amount(self, auth_client, cart_with_off_code, product):
        response = auth_client.post(CHECKOUT_URL)

        expected_total = float(product.final_price) * (1 - 0.20)
        assert float(response.data["total_amount"]) == pytest.approx(expected_total)