"""Example: authenticate and print every workspace and its models.

Run (after setting ANAPLAN_EMAIL / ANAPLAN_PASSWORD in your environment)::

    python examples/list_models.py

Needs a real Anaplan tenant + credentials.
"""

from __future__ import annotations

from _config import build_client


def main() -> None:
    client = build_client()
    workspaces = client.list_workspaces()
    if not workspaces:
        print("No workspaces accessible to this account.")
        return

    for ws in workspaces:
        print(f"Workspace: {ws.get('name')} ({ws.get('id')})")
        for model in client.list_models(ws["id"]):
            print(f"  Model: {model.get('name')} ({model.get('id')})")


if __name__ == "__main__":
    main()
