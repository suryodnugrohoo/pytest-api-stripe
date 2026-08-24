"""Payment Intents: a positive create and a negative missing-parameter case."""
from __future__ import annotations

import pytest

from src.api.client import StripeClient


@pytest.mark.positive
def test_create_payment_intent_succeeds(api_client: StripeClient):
    response = api_client.create_payment_intent(amount=1500, currency="usd")

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["object"] == "payment_intent"
    assert body["id"].startswith("pi_")
    assert body["amount"] == 1500
    assert body["currency"] == "usd"


@pytest.mark.negative
def test_create_payment_intent_missing_amount_is_rejected(api_client: StripeClient):
    # `amount` is required; omitting it must yield a 400 with a helpful error.
    response = api_client.create_payment_intent(currency="usd")

    assert response.status_code == 400, response.text
    error = response.json()["error"]
    assert error["type"] == "invalid_request_error"
    assert error["param"] == "amount"
