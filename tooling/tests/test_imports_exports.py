"""Tests for chunked upload, the run-and-poll lifecycle, and export download."""

from __future__ import annotations

import pytest
import responses

from anaplan_kit import AnaplanClient
from anaplan_kit.errors import AnaplanTaskError

from .conftest import API_BASE, MODEL_ID, WORKSPACE_ID

FILE_BASE = f"{API_BASE}/workspaces/{WORKSPACE_ID}/models/{MODEL_ID}/files"
IMPORT_BASE = f"{API_BASE}/workspaces/{WORKSPACE_ID}/models/{MODEL_ID}/imports"


@responses.activate
def test_upload_file_chunks(client: AnaplanClient, tmp_path) -> None:
    file_path = tmp_path / "data.csv"
    # 25 bytes with a 10-byte chunk size -> 3 chunks.
    file_path.write_bytes(b"x" * 25)

    file_id = "f1"
    base = f"{FILE_BASE}/{file_id}"
    responses.add(responses.POST, base, json={}, status=200)  # declare count
    for chunk_id in range(3):
        responses.add(responses.PUT, f"{base}/chunks/{chunk_id}", status=204)
    responses.add(responses.POST, f"{base}/complete", json={}, status=200)

    count = client.upload_file(
        WORKSPACE_ID, MODEL_ID, file_id, str(file_path), chunk_size=10
    )
    assert count == 3
    # declare(1) + 3 chunk PUTs + complete(1) == 5 calls.
    assert len(responses.calls) == 5
    # The declare call must announce the chunk count.
    assert b'"chunkCount": 3' in responses.calls[0].request.body


@responses.activate
def test_run_action_and_wait_polls_to_complete(client: AnaplanClient) -> None:
    import_id = "imp1"
    tasks_url = f"{IMPORT_BASE}/{import_id}/tasks"
    responses.add(responses.POST, tasks_url, json={"task": {"taskId": "t1"}})

    status_url = f"{tasks_url}/t1"
    # First poll: still running. Second poll: complete + successful.
    responses.add(responses.GET, status_url, json={"task": {"taskState": "IN_PROGRESS"}})
    responses.add(
        responses.GET,
        status_url,
        json={"task": {"taskState": "COMPLETE", "result": {"successful": True}}},
    )

    status = client.run_import(
        WORKSPACE_ID, MODEL_ID, import_id, poll_interval=0
    )
    assert status["taskState"] == "COMPLETE"
    assert status["result"]["successful"] is True
    # POST start + 2 GET polls.
    assert len(responses.calls) == 3


@responses.activate
def test_run_action_failure_raises(client: AnaplanClient) -> None:
    import_id = "imp2"
    tasks_url = f"{IMPORT_BASE}/{import_id}/tasks"
    responses.add(responses.POST, tasks_url, json={"task": {"taskId": "t2"}})
    responses.add(
        responses.GET,
        f"{tasks_url}/t2",
        json={
            "task": {
                "taskState": "COMPLETE",
                "result": {"successful": False, "failureDumpAvailable": True},
            }
        },
    )

    with pytest.raises(AnaplanTaskError) as exc_info:
        client.run_import(WORKSPACE_ID, MODEL_ID, import_id, poll_interval=0)
    assert exc_info.value.task_id == "t2"
    assert exc_info.value.result["successful"] is False


@responses.activate
def test_poll_timeout_raises(client: AnaplanClient) -> None:
    import_id = "imp3"
    status_url = f"{IMPORT_BASE}/{import_id}/tasks/t3"
    responses.add(
        responses.GET, status_url, json={"task": {"taskState": "IN_PROGRESS"}}
    )
    with pytest.raises(AnaplanTaskError):
        # Zero timeout -> deadline already passed after the first poll.
        client.poll_task(
            WORKSPACE_ID, MODEL_ID, "imports", import_id, "t3",
            poll_interval=0, timeout=0,
        )


@responses.activate
def test_start_task_missing_id_raises(client: AnaplanClient) -> None:
    import_id = "imp4"
    responses.add(
        responses.POST, f"{IMPORT_BASE}/{import_id}/tasks", json={"task": {}}
    )
    with pytest.raises(AnaplanTaskError):
        client.start_task(WORKSPACE_ID, MODEL_ID, "imports", import_id)


@responses.activate
def test_download_export_reassembles_chunks(
    client: AnaplanClient, tmp_path
) -> None:
    file_id = "exp1"
    base = f"{FILE_BASE}/{file_id}"
    responses.add(
        responses.GET,
        f"{base}/chunks",
        json={"chunks": [{"id": "0"}, {"id": "1"}]},
    )
    responses.add(responses.GET, f"{base}/chunks/0", body=b"hello,", status=200)
    responses.add(responses.GET, f"{base}/chunks/1", body=b"world", status=200)

    dest = tmp_path / "out.csv"
    written = client.download_export(WORKSPACE_ID, MODEL_ID, file_id, str(dest))
    assert written == str(dest)
    assert dest.read_bytes() == b"hello,world"
