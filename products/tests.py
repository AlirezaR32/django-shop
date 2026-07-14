from django.test import TestCase

# Create your tests here.
import pytest

from .models import Product
from .fixtures import *


# =================================================================
# ProductListView  GET /products
# =================================================================

@pytest.mark.django_db
class TestProductListView:

    def test_get_returns_200(self, api_client, product):
        response = api_client.get(PRODUCTS_URL)

        assert response.status_code == 200

    def test_get_returns_only_active_products(self, api_client, product, inactive_product):
        response = api_client.get(PRODUCTS_URL)
        titles = [p["title"] for p in response.data["results"]]

        assert product.title in titles
        assert inactive_product.title not in titles

    def test_get_default_ordering_is_by_created_at_desc(self, api_client, many_products):
        response = api_client.get(PRODUCTS_URL)
        titles = [p["title"] for p in response.data["results"]]

        assert titles == [p.title for p in reversed(many_products)]

    def test_get_is_paginated_with_default_page_size(self, api_client, category, brand):
        for i in range(15):
            Product.objects.create(
                title=f"Product {i}", price=1000, category=category, brand=brand, is_active=True
            )
        response = api_client.get(PRODUCTS_URL)

        assert response.status_code == 200
        assert len(response.data["results"]) == 10
        assert response.data["count"] == 15

    def test_get_respects_page_size_query_param(self, api_client, category, brand):
        for i in range(15):
            Product.objects.create(
                title=f"Product {i}", price=1000, category=category, brand=brand, is_active=True
            )
        response = api_client.get(PRODUCTS_URL, {"page_size": 5})

        assert len(response.data["results"]) == 5

    def test_filter_by_category(self, api_client, product, other_category_product):
        response = api_client.get(PRODUCTS_URL, {"category": product.category.name})
        titles = [p["title"] for p in response.data["results"]]

        assert product.title in titles
        assert other_category_product.title not in titles

    def test_filter_by_category_is_case_insensitive(self, api_client, product):
        response = api_client.get(PRODUCTS_URL, {"category": product.category.name.upper()})
        titles = [p["title"] for p in response.data["results"]]

        assert product.title in titles

    def test_filter_by_nonexistent_category_returns_404(self, api_client, product):
        response = api_client.get(PRODUCTS_URL, {"category": "NoSuchCategory"})

        assert response.status_code == 404

    def test_filter_by_brand(self, api_client, product, other_category_product):
        response = api_client.get(PRODUCTS_URL, {"brand": product.brand.name})
        titles = [p["title"] for p in response.data["results"]]

        assert product.title in titles
        assert other_category_product.title not in titles

    def test_filter_has_off(self, api_client, product, no_off_product):
        response = api_client.get(PRODUCTS_URL, {"has_off": ""})
        titles = [p["title"] for p in response.data["results"]]

        assert product.title in titles
        assert no_off_product.title not in titles

    def test_filter_is_available(self, api_client, product, out_of_stock_product):
        response = api_client.get(PRODUCTS_URL, {"is_available": ""})
        titles = [p["title"] for p in response.data["results"]]

        assert product.title in titles
        assert out_of_stock_product.title not in titles

    def test_search_by_title(self, api_client, product, other_category_product):
        response = api_client.get(PRODUCTS_URL, {"search": "Headphones"})
        titles = [p["title"] for p in response.data["results"]]

        assert product.title in titles
        assert other_category_product.title not in titles

    def test_sort_by_price_ascending(self, api_client, many_products):
        response = api_client.get(PRODUCTS_URL, {"sort": "price"})
        prices = [p["final_price"] for p in response.data["results"]]

        assert prices == sorted(prices)

    def test_sort_by_price_descending(self, api_client, many_products):
        response = api_client.get(PRODUCTS_URL, {"sort": "price", "descending": "true"})
        prices = [p["final_price"] for p in response.data["results"]]

        assert prices == sorted(prices, reverse=True)

    def test_sort_by_view_count(self, api_client, many_products):
        response = api_client.get(PRODUCTS_URL, {"sort": "view"})
        titles = [p["title"] for p in response.data["results"]]
        expected_order = [p.title for p in sorted(many_products, key=lambda x: x.view_count)]

        assert titles == expected_order

    def test_sort_by_sell_count(self, api_client, many_products):
        response = api_client.get(PRODUCTS_URL, {"sort": "sell"})
        titles = [p["title"] for p in response.data["results"]]
        expected_order = [p.title for p in sorted(many_products, key=lambda x: x.sell_count)]

        assert titles == expected_order

    def test_sort_by_review_point(self, api_client, many_products):
        response = api_client.get(PRODUCTS_URL, {"sort": "point"})
        titles = [p["title"] for p in response.data["results"]]
        expected_order = [p.title for p in sorted(many_products, key=lambda x: x.review_avg_point)]

        assert titles == expected_order


# =================================================================
# ProductDetailView  GET /products/<id>
# =================================================================

@pytest.mark.django_db
class TestProductDetailView:

    def test_get_existing_active_product_returns_200(self, api_client, product):
        response = api_client.get(product_detail_url(product.id))

        assert response.status_code == 200

    def test_get_returns_correct_product_data(self, api_client, product):
        response = api_client.get(product_detail_url(product.id))

        assert response.data["id"] == product.id
        assert response.data["title"] == product.title

    def test_get_includes_nested_category_and_brand(self, api_client, product):
        response = api_client.get(product_detail_url(product.id))

        assert response.data["category"]["name"] == product.category.name
        assert response.data["brand"]["name"] == product.brand.name

    def test_get_includes_images(self, api_client, product, product_image):
        response = api_client.get(product_detail_url(product.id))

        assert len(response.data["images"]) == 1

    def test_get_increments_view_count(self, api_client, product):
        original_view_count = product.view_count

        api_client.get(product_detail_url(product.id))
        product.refresh_from_db()

        assert product.view_count == original_view_count + 1

    def test_get_nonexistent_product_returns_404(self, api_client):
        response = api_client.get(product_detail_url(99999))

        assert response.status_code == 404

    def test_get_inactive_product_returns_404(self, api_client, inactive_product):
        response = api_client.get(product_detail_url(inactive_product.id))

        assert response.status_code == 404