import pytest
from rest_framework.test import APIClient
from .models import Address,User  
from django.urls import reverse
from .models import Address,User  # adjust import to your app name
from .fixtures import *
# =================================================================
# RegisterUserView
# =================================================================

@pytest.mark.django_db
class TestRegisterUserView:

    def test_register_new_user_returns_200(self, api_client, valid_register_payload):
        response = api_client.post(REGISTER_URL, valid_register_payload)

        assert response.status_code == 200
        assert response.data["detail"] == "user been registered successfully."

    def test_register_creates_user_in_db(self, api_client, valid_register_payload):
        api_client.post(REGISTER_URL, valid_register_payload)

        assert User.objects.filter(username="newuser").exists()

    def test_register_duplicate_username_returns_400(self, api_client, user, valid_register_payload):
        # `user` fixture already created "testuser"; try to register same username
        payload = {"username": "testuser", "password": "somepass"}
        response = api_client.post(REGISTER_URL, payload)

        assert response.status_code == 400
        assert "already registered" in response.data["detail"]

    def test_register_duplicate_does_not_create_second_user(self, api_client, user):
        payload = {"username": "testuser", "password": "anotherpass"}
        api_client.post(REGISTER_URL, payload)

        assert User.objects.filter(username="testuser").count() == 1
# =================================================================
# AddressListView  GET /users/addresses/
# =================================================================

@pytest.mark.django_db
class TestAddressListViewGet:

    def test_get_returns_200(self, auth_client, address):
        response = auth_client.get(ADDRESS_LIST_URL)

        assert response.status_code == 200

    def test_get_returns_only_current_users_addresses(
        self, auth_client, address, other_user_address
    ):
        response = auth_client.get(ADDRESS_LIST_URL)
        returned_ids = [a["id"] for a in response.data]

        assert address.id in returned_ids
        assert other_user_address.id not in returned_ids

    def test_get_returns_all_addresses_for_user(
        self, auth_client, address, second_address
    ):
        response = auth_client.get(ADDRESS_LIST_URL)

        assert len(response.data) == 2

    def test_get_returns_empty_list_when_no_addresses(self, auth_client):
        response = auth_client.get(ADDRESS_LIST_URL)

        assert response.status_code == 200
        assert response.data == []


#=================================================================
#AddressListView  POST /users/addresses/
#=================================================================

@pytest.mark.django_db
class TestAddressListViewPost:

    def test_post_creates_address_returns_200(self,auth_client, valid_address_payload):
        response = auth_client.post(ADDRESS_LIST_URL, valid_address_payload)

        assert response.status_code == 200
        assert "added" in response.data["detail"]

    def test_post_first_address_is_set_as_default(self, auth_client, user, valid_address_payload):
        auth_client.post(ADDRESS_LIST_URL, valid_address_payload)

        created = Address.objects.get(user=user)
        assert created.is_default is True

    def test_post_second_address_is_not_set_as_default(
        self, auth_client, user, address, valid_address_payload_2
    ):
        # `address` fixture already created one address for `user`
        auth_client.post(ADDRESS_LIST_URL, valid_address_payload_2)

        second = Address.objects.get(user=user, full_address="456 Side Ave")
        assert second.is_default is False

    def test_post_saves_address_to_db(self, auth_client, user, valid_address_payload):
        auth_client.post(ADDRESS_LIST_URL, valid_address_payload)

        assert Address.objects.filter(user=user).count() == 1



# =================================================================
# AddressDetailView  GET /users/addresses/<id>/
# =================================================================

@pytest.mark.django_db
class TestAddressDetailViewGet:

    def test_get_existing_address_returns_200(self, auth_client, address):
        response = auth_client.get(address_detail_url(address.id))

        assert response.status_code == 200

    def test_get_nonexistent_address_returns_404(self, auth_client):
        response = auth_client.get(address_detail_url(99999))

        assert response.status_code == 404


#=================================================================
#AddressDetailView  PATCH /users/addresses/<id>/
#=================================================================

@pytest.mark.django_db
class TestAddressDetailViewPatch:

    def test_patch_updates_city_returns_200(self, auth_client, address):
        response = auth_client.patch(address_detail_url(address.id), {"city": "Frankfurt"})

        assert response.status_code == 200

    def test_patch_persists_changes_to_db(self, auth_client, address):
        auth_client.patch(address_detail_url(address.id), {"city": "Frankfurt"})
        address.refresh_from_db()

        assert address.city == "Frankfurt"

    def test_patch_setting_is_default_true_updates_default_address(
        self, auth_client , address, second_address
    ):
        """Promoting second_address to default should demote address."""
        auth_client.patch(address_detail_url(second_address.id), {"is_default": True})

        second_address.refresh_from_db()
        address.refresh_from_db()

        assert second_address.is_default is True
        assert address.is_default is False

    def test_patch_nonexistent_address_returns_404(self, auth_client):
        response = auth_client.patch(address_detail_url(99999), {"city": "Nowhere"})

        assert response.status_code == 404
