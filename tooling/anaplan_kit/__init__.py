"""``anaplan_kit`` — a small, typed Python client for the Anaplan REST API v2.

This package wraps the Anaplan *Integration API v2.0*: authentication, listing
workspace/model metadata, chunked file upload/download, and running
imports/exports/actions/processes as asynchronous tasks (start + poll).

.. warning::
   This is an **educational** wrapper. Running anything against a live tenant
   requires a real Anaplan account, workspace and model, plus credentials
   supplied via environment variables (see ``.env.example``). Nothing here
   talks to a network until you call a method with real IDs.

Typical usage::

    from anaplan_kit import AnaplanClient, Authenticator

    client = AnaplanClient.from_credentials(email, password)
    for ws in client.list_workspaces():
        print(ws["id"], ws["name"])
"""

from __future__ import annotations

from .auth import Authenticator, AuthToken
from .client import AnaplanClient
from .errors import (
    AnaplanAPIError,
    AnaplanAuthError,
    AnaplanError,
    AnaplanTaskError,
)

__version__ = "0.1.0"

__all__ = [
    "AnaplanClient",
    "Authenticator",
    "AuthToken",
    "AnaplanError",
    "AnaplanAuthError",
    "AnaplanAPIError",
    "AnaplanTaskError",
    "__version__",
]
