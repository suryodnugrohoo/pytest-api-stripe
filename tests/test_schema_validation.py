"""Schema validation: responses must match a consistent JSON structure."""
from __future__ import annotations

import pytest

from src.api.client import StripeClient
from src.schemas import validate_schema

pytestmark = pytest.mark.schema


def test_customer_object_matches_schema(created_customer: dict):
    # Raises jsonschema.ValidationError (failing the test) on any mismatch.
    validate_schema(created_customer, "customer")


def test_customer_list_matches_schema(api_client: StripeClient):
    response = api_client.list_customers(limit=2)
    assert response.status_code == 200, response.text
    validate_schema(response.json(), "list")


def test_payment_intent_matches_schema(api_client: StripeClient):
    response = api_client.create_payment_intent(amount=2000, currency="eur")
    assert response.status_code == 200, response.text
    validate_schema(response.json(), "payment_intent")
