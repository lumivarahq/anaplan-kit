"""Example: run a process (ordered group of actions) and wait for it.

Run::

    python examples/run_process.py <processId>

Needs a real Anaplan tenant + credentials.
"""

from __future__ import annotations

import sys

from _config import build_client, require_env


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python run_process.py <processId>")
    process_id = sys.argv[1]

    workspace_id = require_env("ANAPLAN_WORKSPACE_ID")
    model_id = require_env("ANAPLAN_MODEL_ID")
    client = build_client()

    status = client.run_process(workspace_id, model_id, process_id)
    result = status.get("result", {})
    print(f"Process complete. successful={result.get('successful')}")


if __name__ == "__main__":
    main()
