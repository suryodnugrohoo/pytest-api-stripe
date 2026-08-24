"""Performance checks: log and assert response time stays within budget."""
from __future__ import annotations

import logging

import pytest

from src.api.client import StripeClient
from src.config.settings import Settings

pytestmark = pytest.mark.performance

logger = logging.getLogger("performance")


def _elapsed_ms(response) -> float:
    return response.elapsed.total_seconds() * 1000


def test_list_customers_within_threshold(api_client: StripeClient, settings: Settings):
    response = api_client.list_customers(limit=1)
    elapsed = _elapsed_ms(response)
    logger.info("GET /customers took %.0f ms (budget %d ms)", elapsed, settings.perf_threshold_ms)

    assert response.status_code == 200, response.text
    assert elapsed < settings.perf_threshold_ms, (
        f"Response time {elapsed:.0f} ms exceeded budget {settings.perf_threshold_ms} ms"
    )


def test_create_customer_within_threshold(api_client: StripeClient, settings: Settings):
    response = api_client.create_customer(email="perf+check@example.com", name="Perf Check")
    elapsed = _elapsed_ms(response)
    logger.info("POST /customers took %.0f ms (budget %d ms)", elapsed, settings.perf_threshold_ms)

    assert response.status_code == 200, response.text
    assert elapsed < settings.perf_threshold_ms, (
        f"Response time {elapsed:.0f} ms exceeded budget {settings.perf_threshold_ms} ms"
    )

    api_client.delete_customer(response.json()["id"])
