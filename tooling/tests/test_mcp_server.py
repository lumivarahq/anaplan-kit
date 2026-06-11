"""Tests for the MCP server tools.

Offline like everything else: knowledge tools read the repo's own Markdown,
live-tool happy paths mock HTTP with ``responses``, and the no-credentials
honesty invariant is asserted explicitly (offline mode, no network attempted).

Requires the ``[mcp]`` extra; skipped cleanly when the SDK is not installed.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import responses

pytest.importorskip("mcp", reason="MCP SDK not installed (pip install -e '.[mcp]')")

from anaplan_kit import kitindex, mcp_server  # noqa: E402  (after importorskip)

REPO_ROOT = Path(__file__).resolve().parents[2]

AUTH_URL = "https://auth.test.local/token/authenticate"
API_BASE = "https://api.test.local/2/0"


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin the kit root and guarantee no Anaplan credentials are configured."""
    monkeypatch.setenv(kitindex.ENV_ROOT, str(REPO_ROOT))
    for var in (
        mcp_server.ENV_EMAIL,
        mcp_server.ENV_PASSWORD,
        mcp_server.ENV_WORKSPACE,
        mcp_server.ENV_MODEL,
        mcp_server.ENV_AUTH_URL,
        mcp_server.ENV_API_BASE,
    ):
        monkeypatch.delenv(var, raising=False)


def _set_live_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(mcp_server.ENV_EMAIL, "tester@example.com")
    monkeypatch.setenv(mcp_server.ENV_PASSWORD, "secret")  # noqa: S105 - dummy test value
    monkeypatch.setenv(mcp_server.ENV_AUTH_URL, AUTH_URL)
    monkeypatch.setenv(mcp_server.ENV_API_BASE, API_BASE)


def _mock_auth() -> None:
    responses.add(
        responses.POST,
        AUTH_URL,
        json={"tokenInfo": {"tokenValue": "FAKE-TOKEN", "expiresAt": 9999999999999}},
        status=200,
    )


# --- server wiring ----------------------------------------------------------


def test_console_entrypoint_exists() -> None:
    assert callable(mcp_server.main)
    assert mcp_server.mcp.name == "anaplan-kit"


# --- offline knowledge tools --------------------------------------------------


def test_search_kit_returns_ranked_results() -> None:
    result = mcp_server.search_kit("rolling forecast", area="cookbook")
    assert result["results"]
    assert all(r["path"].startswith("cookbook/") for r in result["results"])


def test_read_kit_doc_reads_a_doc() -> None:
    result = mcp_server.read_kit_doc("docs/02-formulas/README.md")
    assert "Formulas" in result["content"]


def test_read_kit_doc_rejects_escape_as_structured_error() -> None:
    result = mcp_server.read_kit_doc("../../../etc/passwd.md")
    assert "error" in result
    assert "content" not in result


def test_read_kit_doc_rejects_non_markdown() -> None:
    result = mcp_server.read_kit_doc("tooling/pyproject.toml")
    assert "error" in result


def test_formula_reference_finds_known_function() -> None:
    result = mcp_server.formula_reference("LOOKUP")
    assert result["found"] is True
    assert result["matches"][0]["path"].startswith("docs/02-formulas/")


def test_list_recipes_tool() -> None:
    result = mcp_server.list_recipes(area="time-and-forecasting")
    assert result["count"] == len(result["recipes"]) > 0


def test_lint_blueprint_flags_convention_violation() -> None:
    # Deliberate violations: a non-DISCO prefix (BAD_PREFIX) and the
    # 'Is Actual Month?' naming the kit warns about (IS_ACTUAL_NAME).
    content = (
        "## XYZ01 Bad Module\n"
        "\n"
        "| Line Item | Format | Summary | Applies To | Formula |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Is Actual Month? | Boolean | — | Time | — |\n"
    )
    result = mcp_server.lint_blueprint(content)
    assert result["modules_parsed"] == 1
    codes = {f["code"] for f in result["findings"]}
    assert "BAD_PREFIX" in codes
    assert "IS_ACTUAL_NAME" in codes
    assert result["ok"] is False


def test_lint_blueprint_clean_table_is_ok() -> None:
    content = (
        "## CAL01 Revenue\n"
        "\n"
        "| Line Item | Format | Summary | Applies To | Formula |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Gross Revenue | Number | Sum | Time | `Volume * Price` |\n"
    )
    result = mcp_server.lint_blueprint(content)
    assert result["modules_parsed"] == 1
    assert result["ok"] is True


# --- offline honesty invariant (load-bearing) ------------------------------------


def test_connection_status_offline_without_creds() -> None:
    status = mcp_server.anaplan_connection_status()
    assert status["mode"] == "offline"
    assert status["configured"][mcp_server.ENV_EMAIL] is False
    # No credential *values* anywhere in the response.
    assert "tester" not in str(status)


def test_connection_status_never_reveals_values(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_live_env(monkeypatch)
    status = mcp_server.anaplan_connection_status()
    assert status["mode"] == "live"
    assert status["configured"][mcp_server.ENV_PASSWORD] is True
    assert "secret" not in str(status)
    assert "tester@example.com" not in str(status)


@responses.activate  # zero registered mocks: any HTTP attempt would error loudly
def test_live_tools_return_offline_without_creds() -> None:
    for result in (
        mcp_server.anaplan_list_workspaces(),
        mcp_server.anaplan_list_models(workspace_id="ws123"),
        mcp_server.anaplan_model_metadata(model_id="m456", workspace_id="ws123"),
        mcp_server.anaplan_run_action("a1", workspace_id="ws123", model_id="m456"),
        mcp_server.anaplan_run_import("i1", workspace_id="ws123", model_id="m456"),
        mcp_server.anaplan_run_export("e1", workspace_id="ws123", model_id="m456"),
        mcp_server.anaplan_run_process("p1", workspace_id="ws123", model_id="m456"),
    ):
        assert result["mode"] == "offline"
        assert result["error"] == "no Anaplan credentials configured"
    assert len(responses.calls) == 0  # the invariant: no network was attempted


# --- live happy paths (mocked HTTP) ------------------------------------------------


@responses.activate
def test_list_workspaces_live(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_live_env(monkeypatch)
    _mock_auth()
    responses.add(
        responses.GET,
        f"{API_BASE}/workspaces",
        json={"workspaces": [{"id": "ws123", "name": "WS"}]},
        status=200,
    )
    result = mcp_server.anaplan_list_workspaces()
    assert result["mode"] == "live"
    assert result["workspaces"][0]["id"] == "ws123"


@responses.activate
def test_list_models_live_uses_env_workspace(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_live_env(monkeypatch)
    monkeypatch.setenv(mcp_server.ENV_WORKSPACE, "ws123")
    _mock_auth()
    responses.add(
        responses.GET,
        f"{API_BASE}/workspaces/ws123/models",
        json={"models": [{"id": "m456", "name": "Model"}]},
        status=200,
    )
    result = mcp_server.anaplan_list_models()
    assert result["mode"] == "live"
    assert result["workspace_id"] == "ws123"
    assert result["models"][0]["id"] == "m456"


def test_list_models_missing_workspace_is_structured(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_live_env(monkeypatch)
    result = mcp_server.anaplan_list_models()
    assert "error" in result
    assert mcp_server.ENV_WORKSPACE in result["error"]


@responses.activate
def test_model_metadata_live(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_live_env(monkeypatch)
    _mock_auth()
    base = f"{API_BASE}/workspaces/ws123/models/m456"
    for resource, key in (
        ("files", "files"),
        ("imports", "imports"),
        ("exports", "exports"),
        ("actions", "actions"),
        ("processes", "processes"),
    ):
        responses.add(
            responses.GET,
            f"{base}/{resource}",
            json={key: [{"id": f"{resource}-1", "name": resource}]},
            status=200,
        )
    result = mcp_server.anaplan_model_metadata(model_id="m456", workspace_id="ws123")
    assert result["mode"] == "live"
    assert result["imports"][0]["id"] == "imports-1"
    assert result["processes"][0]["name"] == "processes"


@responses.activate
def test_run_process_live(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_live_env(monkeypatch)
    _mock_auth()
    base = f"{API_BASE}/workspaces/ws123/models/m456/processes/p1/tasks"
    responses.add(responses.POST, base, json={"task": {"taskId": "t1"}}, status=200)
    responses.add(
        responses.GET,
        f"{base}/t1",
        json={"task": {"taskId": "t1", "taskState": "COMPLETE", "result": {"successful": True}}},
        status=200,
    )
    result = mcp_server.anaplan_run_process("p1", workspace_id="ws123", model_id="m456")
    assert result["mode"] == "live"
    assert result["task"]["taskState"] == "COMPLETE"


@responses.activate
def test_live_api_error_is_structured_not_raised(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_live_env(monkeypatch)
    _mock_auth()
    responses.add(
        responses.GET,
        f"{API_BASE}/workspaces",
        json={"status": {"code": 403, "message": "forbidden"}},
        status=403,
    )
    result = mcp_server.anaplan_list_workspaces()
    assert result["mode"] == "live"
    assert "error" in result
    assert "403" in result["error"]
