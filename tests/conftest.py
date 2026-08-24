"""Shared pytest fixtures for the Stripe API suite."""
from __future__ import annotations

import time
from typing import Iterator

import pytest

from src.api.client import StripeClient
from src.config.settings import Settings, get_settings


def unique_email() -> str:
    """A unique email per call so created customers never collide."""
    return f"qa+{int(time.time() * 1000)}@example.com"


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings: Settings) -> StripeClient:
    """A client authenticated with the configured (valid) test key."""
    return StripeClient(settings.base_url, settings.api_key)


@pytest.fixture(scope="session")
def bad_key_client(settings: Settings) -> StripeClient:
    """A client using a deliberately invalid key, for auth-failure tests."""
    return StripeClient(settings.base_url, "sk_test_invalid_key_000")


@pytest.fixture
def created_customer(api_client: StripeClient) -> Iterator[dict]:
    """Create a customer for a test and clean it up afterwards."""
    response = api_client.create_customer(email=unique_email(), name="QA Tester")
    assert response.status_code == 200, response.text
    customer = response.json()
    yield customer
    # Teardown: best-effort delete so the test account stays tidy.
    api_client.delete_customer(customer["id"])
