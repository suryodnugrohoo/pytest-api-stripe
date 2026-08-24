from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str
    api_key: str
    perf_threshold_ms: int


def get_settings() -> Settings:
    """Build Settings from the environment, failing fast if the key is missing."""
    api_key = os.getenv("STRIPE_SECRET_KEY")
    if not api_key:
        raise RuntimeError(
            "STRIPE_SECRET_KEY is not set. Copy .env.example to .env and add your "
            "Stripe TEST secret key (sk_test_...)."
        )
    return Settings(
        base_url=os.getenv("STRIPE_BASE_URL", "https://api.stripe.com/v1"),
        api_key=api_key,
        perf_threshold_ms=int(os.getenv("PERF_THRESHOLD_MS", "1000")),
    )
