import pytest
from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User
from products.models import Product, Category, Brand, OffCode
from carts.models import Cart, CartItem

from .models import Order, OrderItem

# =================================================================
# URL helpers
# =================================================================

ORDER_LIST_URL = reverse("order-list")
CHECKOUT_URL = reverse("checkout")


def order_detail_url(order_id):
    return reverse("order-detail", args=[order_id])


def cancel_order_url(order_id):
    return reverse("cancell-order", args=[order_id])


# =================================================================
# Client / auth fixtures
# =================================================================

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="otheruser", password="testpass123")


def _authenticated_client(django_user):
    client = APIClient()
    token_url = reverse("get-token")
    response = client.post(
        token_url, {"username": django_user.username, "password": "testpass123"}
    )
    access_token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.fixture
def auth_client(user):
    return _authenticated_client(user)


@pytest.fixture
def other_auth_client(other_user):
    return _authenticated_client(other_user)


# =================================================================
# Product fixtures
# =================================================================

@pytest.fixture
def category(db):
    return Category.objects.create(name="Electronics")


@pytest.fixture
def brand(db):
    return Brand.objects.create(name="Sony")


@pytest.fixture
def product(db, category, brand):
    return Product.objects.create(
        title="Wireless Headphones",
        price=10000,
        category=category,
        brand=brand,
        stock_quantity=10,
        is_active=True,
    )


@pytest.fixture
def other_product(db, category, brand):
    return Product.objects.create(
        title="Bluetooth Speaker",
        price=8000,
        category=category,
        brand=brand,
        stock_quantity=10,
        is_active=True,
    )


@pytest.fixture
def valid_off_code(db):
    return OffCode.objects.create(code="SAVE20", off_percent=Decimal("0.20"))


# =================================================================
# Cart fixtures (checkout reads from the user's active cart)
# =================================================================

@pytest.fixture
def cart(db, user):
    return Cart.objects.create(user=user)


@pytest.fixture
def cart_with_item(db, cart, product):
    CartItem.objects.create(cart=cart, product=product, quantity=Decimal("2"))
    return cart


@pytest.fixture
def cart_with_two_understocked_items(db, cart, product, other_product):
    """
    Both items request more than is in stock -- used to expose the
    services.py bug where only one stock error survives in the dict.
    """
    CartItem.objects.create(
        cart=cart, product=product, quantity=Decimal(product.stock_quantity + 5)
    )
    CartItem.objects.create(
        cart=cart, product=other_product, quantity=Decimal(other_product.stock_quantity + 5)
    )
    return cart


@pytest.fixture
def cart_with_off_code(db, cart, product, valid_off_code):
    CartItem.objects.create(cart=cart, product=product, quantity=Decimal("1"))
    cart.off_code = valid_off_code
    cart.save(update_fields=["off_code"])
    return cart


# =================================================================
# Order fixtures
# =================================================================

@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user, total_amount="10000")


@pytest.fixture
def order_item(db, order, product):
    return OrderItem.objects.create(order=order, product=product, quantity=Decimal("2"))


@pytest.fixture
def other_user_order(db, other_user):
    return Order.objects.create(user=other_user, total_amount="5000")


@pytest.fixture
def completed_order(db, user):
    return Order.objects.create(user=user, total_amount="10000", status="COMPLETED")


@pytest.fixture
def cancelled_order(db, user):
    return Order.objects.create(user=user, total_amount="10000", status="CANCELLED")