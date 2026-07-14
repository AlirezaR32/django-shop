import pytest
from decimal import Decimal
from datetime import timedelta

from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User
from products.models import Product, Category, Brand, OffCode

from .models import Cart, CartItem

# =================================================================
# URL helpers
# =================================================================

CART_URL = reverse("get-cart")
APPLY_OFF_CODE_URL = reverse("apply-off-code-to-cart")


def cart_item_url(item_id):
    return reverse("change-cart", args=[item_id])


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
    """Authenticated client for `user`."""
    return _authenticated_client(user)


@pytest.fixture
def other_auth_client(other_user):
    """Authenticated client for `other_user` -- for cross-user/permission tests."""
    return _authenticated_client(other_user)


# =================================================================
# Product fixtures (minimal set needed for cart tests)
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
        stock_quantity=5,
        is_active=True,
    )


@pytest.fixture
def other_product(db, category, brand):
    return Product.objects.create(
        title="Bluetooth Speaker",
        price=8000,
        category=category,
        brand=brand,
        stock_quantity=3,
        is_active=True,
    )


@pytest.fixture
def out_of_stock_product(db, category, brand):
    return Product.objects.create(
        title="Sold Out Mouse",
        price=1500,
        category=category,
        brand=brand,
        stock_quantity=0,
        is_active=True,
    )


@pytest.fixture
def inactive_product(db, category, brand):
    return Product.objects.create(
        title="Discontinued Keyboard",
        price=2000,
        category=category,
        brand=brand,
        stock_quantity=10,
        is_active=False,
    )


# =================================================================
# OffCode fixtures
# =================================================================

@pytest.fixture
def valid_off_code(db):
    return OffCode.objects.create(code="SAVE20", off_percent=Decimal("0.20"))


@pytest.fixture
def expired_off_code(db):
    """An OffCode whose default 1-day expire_duration has already passed."""
    off_code = OffCode.objects.create(code="OLDCODE", off_percent=Decimal("0.10"))
    OffCode.objects.filter(pk=off_code.pk).update(
        created_at=timezone.now() - timedelta(days=2)
    )
    off_code.refresh_from_db()
    return off_code


# =================================================================
# Cart / CartItem fixtures
# =================================================================

@pytest.fixture
def cart(db, user):
    return Cart.objects.create(user=user)


@pytest.fixture
def inactive_cart(db, user):
    return Cart.objects.create(user=user, is_active=False)


@pytest.fixture
def cart_item(db, cart, product):
    return CartItem.objects.create(cart=cart, product=product, quantity=Decimal("2"))


@pytest.fixture
def other_user_cart(db, other_user):
    return Cart.objects.create(user=other_user)


@pytest.fixture
def other_user_cart_item(db, other_user_cart, other_product):
    return CartItem.objects.create(
        cart=other_user_cart, product=other_product, quantity=Decimal("1")
    )