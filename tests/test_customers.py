"""Positive flows for the Customers resource: successful responses + correct data."""
from __future__ import annotations

import pytest

from src.api.client import StripeClient
from tests.conftest import unique_email

pytestmark = pytest.mark.positive


def test_create_customer_returns_expected_data(api_client: StripeClient):
    email = unique_email()
    response = api_client.create_customer(email=email, name="Ada Lovelace")

    assert response.status_code == 200, response.text
    body = response.json()
    # Correct data values, not just a 2xx.
    assert body["object"] == "customer"
    assert body["id"].startswith("cus_")
    assert body["email"] == email
    assert body["name"] == "Ada Lovelace"
    assert body["livemode"] is False  # test mode

    # Cleanup.
    api_client.delete_customer(body["id"])


def test_retrieve_customer_matches_created(api_client: StripeClient, created_customer: dict):
    response = api_client.get_customer(created_customer["id"])

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["id"] == created_customer["id"]
    assert body["email"] == created_customer["email"]


def test_list_customers_returns_collection(api_client: StripeClient, created_customer: dict):
    response = api_client.list_customers(limit=3)

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["object"] == "list"
    assert isinstance(body["data"], list)
    assert len(body["data"]) <= 3
