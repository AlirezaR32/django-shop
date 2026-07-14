import pytest
from decimal import Decimal
from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APIClient

from .models import Product, Category, Brand, Image

# =================================================================
# URL helpers
# =================================================================
# NOTE: urls.py has no `name=` on these paths and there's no visible
# project-level urls.py, so these are hardcoded to match urls.py as given.
# Adjust the prefix here if this app is mounted under e.g. /api/.

PRODUCTS_URL = "/products"


def product_detail_url(product_id):
    return f"/products/{product_id}"


# =================================================================
# Client fixture
# =================================================================

@pytest.fixture
def api_client():
    return APIClient()


# =================================================================
# Category / Brand fixtures
# =================================================================

@pytest.fixture
def category(db):
    return Category.objects.create(name="Electronics")


@pytest.fixture
def other_category(db):
    return Category.objects.create(name="Books")


@pytest.fixture
def brand(db):
    return Brand.objects.create(name="Sony")


@pytest.fixture
def other_brand(db):
    return Brand.objects.create(name="Samsung")


# =================================================================
# Product fixtures
# =================================================================

@pytest.fixture
def product(db, category, brand):
    return Product.objects.create(
        title="Wireless Headphones",
        short_desc="Noise-cancelling headphones",
        desc="A great pair of wireless headphones.",
        price=10000,
        off_percent=Decimal("0.20"),
        category=category,
        brand=brand,
        stock_quantity=5,
        review_avg_point=Decimal("4.50"),
        view_count=10,
        sell_count=3,
        is_active=True,
    )


@pytest.fixture
def inactive_product(db, category, brand):
    return Product.objects.create(
        title="Discontinued Speaker",
        price=5000,
        category=category,
        brand=brand,
        stock_quantity=0,
        is_active=False,
    )


@pytest.fixture
def out_of_stock_product(db, category, brand):
    return Product.objects.create(
        title="Sold Out Keyboard",
        price=3000,
        category=category,
        brand=brand,
        stock_quantity=0,
        is_active=True,
    )


@pytest.fixture
def no_off_product(db, category, brand):
    return Product.objects.create(
        title="Plain Mouse",
        price=1500,
        category=category,
        brand=brand,
        stock_quantity=20,
        off_percent=Decimal("0.00"),
        is_active=True,
    )


@pytest.fixture
def other_category_product(db, other_category, other_brand):
    return Product.objects.create(
        title="Python Programming Book",
        price=2000,
        category=other_category,
        brand=other_brand,
        stock_quantity=15,
        is_active=True,
    )


@pytest.fixture
def product_image(db, product):
    return Image.objects.create(product=product, image="products/headphones.jpg")


@pytest.fixture
def many_products(db, category, brand):
    """
    A batch of active products with distinct price/view/sell/review values
    and explicit, spread-out created_at timestamps -- useful for testing
    sort ordering (including the default '-created_at' ordering) without
    flakiness from near-identical auto_now_add timestamps.
    """
    data = [
        {"title": "Product A", "price": 1000, "view_count": 5, "sell_count": 1, "review_avg_point": Decimal("2.00")},
        {"title": "Product B", "price": 3000, "view_count": 20, "sell_count": 10, "review_avg_point": Decimal("4.00")},
        {"title": "Product C", "price": 2000, "view_count": 1, "sell_count": 5, "review_avg_point": Decimal("3.00")},
    ]

    products = []
    for entry in data:
        products.append(
            Product.objects.create(
                category=category,
                brand=brand,
                stock_quantity=10,
                is_active=True,
                **entry,
            )
        )

    # Force distinct, ordered created_at values (A oldest, C newest)
    base_time = timezone.now()
    for index, prod in enumerate(products):
        Product.objects.filter(pk=prod.pk).update(
            created_at=base_time - timedelta(minutes=(len(products) - index))
        )
        prod.refresh_from_db()

    return products