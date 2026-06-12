import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Address,User  # adjust import to your app name


# ──────────────────────────────────────────────
# Client fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def api_client():
    """Unauthenticated API client."""
    return APIClient()


@pytest.fixture
def auth_client(user):
    """Authenticated API client for `user`."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


# ──────────────────────────────────────────────
# User fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def user(db):
    """A plain registered user."""
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def other_user(db):
    """A second user, useful for isolation tests."""
    return User.objects.create_user(username="otheruser", password="otherpass123")


# ──────────────────────────────────────────────
# Payload fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def valid_register_payload():
    return {"username": "newuser", "password": "newpass123"}


@pytest.fixture
def valid_address_payload():
    return {
        "full_address": "123 Main St",
        "city": "Berlin",
        "state": "Berlin",
        "postal_code": "10115",
    }


@pytest.fixture
def valid_address_payload_2():
    """A second distinct address payload."""
    return {
        "full_address": "456 Side Ave",
        "city": "Hamburg",
        "state": "Hamburg",
        "postal_code": "20095",
        "longtiude": 10,
    }


# ──────────────────────────────────────────────
# Address fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def address(db, user):
    """One address belonging to `user`, marked as default."""
    return Address.objects.create(
        user=user,
        full_address="123 Main St",
        city="Berlin",
        state="Berlin",
        postal_code="10115",
        longtiude=13,
        is_default=True,
    )


@pytest.fixture
def second_address(db, user):
    """A non-default second address belonging to `user`."""
    return Address.objects.create(
        user=user,
        full_address="456 Side Ave",
        city="Hamburg",
        state="Hamburg",
        postal_code="20095",
        longtiude=10,
        is_default=False,
    )


@pytest.fixture
def other_user_address(db, other_user):
    """An address belonging to `other_user`."""
    return Address.objects.create(
        user=other_user,
        full_address="789 Other Rd",
        city="Munich",
        state="Bavaria",
        postal_code="80331",
        longtiude=11,
        is_default=True,
    )