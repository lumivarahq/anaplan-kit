"""Shared helpers for the example scripts.

Reads credentials and IDs from environment variables (see ``.env.example``)
and builds an :class:`~anaplan_kit.AnaplanClient`. No secrets are ever
hard-coded.

.. warning::
   These examples make **real network calls** to Anaplan. They need a live
   tenant and valid credentials to do anything useful — they are illustrative,
   not runnable offline.
"""

from __future__ import annotations

import os
import sys

from anaplan_kit import AnaplanClient


def require_env(name: str) -> str:
    """Return an environment variable's value or exit with a clear message."""
    value = os.environ.get(name)
    if not value:
        sys.exit(
            f"Missing required environment variable {name!r}. "
            f"Copy .env.example to .env and set it (or export it)."
        )
    return value


def build_client() -> AnaplanClient:
    """Construct an authenticated client from environment variables."""
    email = require_env("ANAPLAN_EMAIL")
    password = require_env("ANAPLAN_PASSWORD")
    return AnaplanClient.from_credentials(email=email, password=password)
