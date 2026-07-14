import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from .models import User, Address

# =================================================================
# URL helpers
# =================================================================

REGISTER_URL = reverse("register")
TOKEN_URL = reverse("get-token")
ADDRESS_LIST_URL = reverse("address-list")


def address_detail_url(address_id):
    return reverse("address-detail", args=[address_id])


# =================================================================
# Client fixtures
# =================================================================

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client, user):
    """
    An APIClient already carrying a valid JWT access token for `user`.
    """
    response = api_client.post(
        TOKEN_URL, {"username": user.username, "password": "testpass123"}
    )
    access_token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


# =================================================================
# User fixtures
# =================================================================

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="otheruser", password="testpass123")


# =================================================================
# Payload fixtures
# =================================================================

@pytest.fixture
def valid_register_payload():
    return {"username": "newuser", "password": "newpass123"}


@pytest.fixture
def valid_address_payload():
    return {
        "full_address": "123 Main St",
        "city": "Berlin",
        "state": "Berlin",
    }


@pytest.fixture
def valid_address_payload_2():
    return {
        "full_address": "456 Side Ave",
        "city": "Munich",
        "state": "Bavaria",
    }


# =================================================================
# Address model fixtures
# =================================================================

@pytest.fixture
def address(db, user):
    return Address.objects.create(
        user=user,
        full_address="123 Main St",
        city="Berlin",
        state="Berlin",
        is_default=True,
    )


@pytest.fixture
def second_address(db, user):
    return Address.objects.create(
        user=user,
        full_address="456 Side Ave",
        city="Munich",
        state="Bavaria",
        is_default=False,
    )


@pytest.fixture
def other_user_address(db, other_user):
    return Address.objects.create(
        user=other_user,
        full_address="789 Other Rd",
        city="Hamburg",
        state="Hamburg",
        is_default=True,
    )