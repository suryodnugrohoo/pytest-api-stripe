"""Negative auth flow: an invalid API key must be rejected with 401."""
from __future__ import annotations

import pytest

from src.api.client import StripeClient

pytestmark = pytest.mark.negative


def test_invalid_api_key_is_unauthorized(bad_key_client: StripeClient):
    response = bad_key_client.list_customers()

    assert response.status_code == 401, response.text
    error = response.json()["error"]
    assert error["type"] == "invalid_request_error"
    # Stripe echoes an actionable message for a bad key.
    assert "Invalid API Key" in error["message"]
