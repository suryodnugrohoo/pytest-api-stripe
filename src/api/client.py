from __future__ import annotations

import logging
from typing import Any

import requests

logger = logging.getLogger("stripe_client")


class StripeClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        # Stripe accepts the secret key as a Bearer token.
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    # --- low-level verbs ------------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        response = self.session.request(method, self._url(path), timeout=self.timeout, **kwargs)
        logger.info(
            "%s %s -> %s in %.0f ms",
            method,
            path,
            response.status_code,
            response.elapsed.total_seconds() * 1000,
        )
        return response

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        return self._request("GET", path, params=params)

    def post(self, path: str, data: dict | None = None) -> requests.Response:
        return self._request("POST", path, data=data)

    def delete(self, path: str) -> requests.Response:
        return self._request("DELETE", path)

    # --- resource helpers -----------------------------------------------------

    def create_customer(self, **fields: Any) -> requests.Response:
        return self.post("/customers", data=fields)

    def get_customer(self, customer_id: str) -> requests.Response:
        return self.get(f"/customers/{customer_id}")

    def list_customers(self, limit: int = 3) -> requests.Response:
        return self.get("/customers", params={"limit": limit})

    def delete_customer(self, customer_id: str) -> requests.Response:
        return self.delete(f"/customers/{customer_id}")

    def create_payment_intent(self, **fields: Any) -> requests.Response:
        return self.post("/payment_intents", data=fields)
