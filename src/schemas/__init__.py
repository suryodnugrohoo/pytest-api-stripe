"""JSON Schema loading + validation helpers.

Schemas live as `.json` files next to this module so the response structure is
documented declaratively and validated with the `jsonschema` library.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any

from jsonschema import validate

_SCHEMA_DIR = pathlib.Path(__file__).parent


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((_SCHEMA_DIR / f"{name}.json").read_text(encoding="utf-8"))


def validate_schema(instance: Any, schema_name: str) -> None:
    """Raise jsonschema.ValidationError if `instance` violates the named schema."""
    validate(instance=instance, schema=load_schema(schema_name))
