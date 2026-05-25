"""Tests for the core ``_request`` path: success, errors, retries, headers."""

from __future__ import annotations

import pytest
import responses
from requests.exceptions import ConnectionError as ReqConnectionError

from anaplan_kit import AnaplanClient
from anaplan_kit.errors import AnaplanAPIError

from .conftest import API_BASE, WORKSPACE_ID


@responses.activate
def test_request_success_parses_json(client: AnaplanClient) -> None:
    responses.add(
        responses.GET,
        f"{API_BASE}/workspaces",
        json={"workspaces": [{"id": WORKSPACE_ID, "name": "WS"}]},
        status=200,
    )
    body = client._request("GET", "/workspaces")
    assert body["workspaces"][0]["id"] == WORKSPACE_ID

    # The bearer token must be attached using the Anaplan scheme.
    sent = responses.calls[0].request
    assert sent.headers["Authorization"] == "AnaplanAuthToken FAKE-TOKEN"


@responses.activate
def test_request_error_status_raises(client: AnaplanClient) -> None:
    responses.add(
        responses.GET,
        f"{API_BASE}/workspaces",
        json={"status": {"code": 404, "message": "not found"}},
        status=404,
    )
    with pytest.raises(AnaplanAPIError) as exc_info:
        client._request("GET", "/workspaces")
    assert exc_info.value.status_code == 404
    assert exc_info.value.payload is not None


@responses.activate
def test_request_empty_body_returns_empty_dict(client: AnaplanClient) -> None:
    responses.add(responses.POST, f"{API_BASE}/ping", body="", status=204)
    assert client._request("POST", "/ping") == {}


@responses.activate
def test_request_non_json_when_expected_raises(client: AnaplanClient) -> None:
    responses.add(responses.GET, f"{API_BASE}/bad", body="<html>nope</html>", status=200)
    with pytest.raises(AnaplanAPIError):
        client._request("GET", "/bad")


@responses.activate
def test_request_raw_bytes(client: AnaplanClient) -> None:
    responses.add(responses.GET, f"{API_BASE}/raw", body=b"\x00\x01\x02", status=200)
    assert client._request("GET", "/raw", expect_json=False) == b"\x00\x01\x02"


@responses.activate
def test_retry_then_succeed(client: AnaplanClient) -> None:
    # First attempt is a transient connection error; second succeeds.
    responses.add(responses.GET, f"{API_BASE}/r", body=ReqConnectionError("boom"))
    responses.add(responses.GET, f"{API_BASE}/r", json={"ok": True}, status=200)

    assert client._request("GET", "/r") == {"ok": True}
    assert len(responses.calls) == 2


@responses.activate
def test_retry_exhausted_raises(client: AnaplanClient) -> None:
    for _ in range(client.max_retries):
        responses.add(responses.GET, f"{API_BASE}/r", body=ReqConnectionError("boom"))
    with pytest.raises(AnaplanAPIError):
        client._request("GET", "/r")
    assert len(responses.calls) == client.max_retries


def test_url_join_and_passthrough(client: AnaplanClient) -> None:
    assert client._url("/workspaces") == f"{API_BASE}/workspaces"
    assert client._url("workspaces") == f"{API_BASE}/workspaces"
    assert client._url("https://x/y") == "https://x/y"
