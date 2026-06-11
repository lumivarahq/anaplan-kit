#!/usr/bin/env python3
"""Check that every relative Markdown link in the repo resolves to a real file.

Pure-Python, no dependencies. Scans all ``*.md`` files under the given root
(default: current directory), and for each ``[text](target)`` link that is a
relative path (not http(s)/mailto/anchor), verifies the target exists.

Exit code: 0 if all links resolve, 1 if any are broken (CI-friendly).

Usage::

    python tools/check_links.py [root]
"""

from __future__ import annotations

import os
import re
import sys

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")


def check(root: str = ".") -> int:
    broken: list[tuple[str, str]] = []
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip VCS dirs, hidden dirs (e.g. tooling/.venv) and vendored deps —
        # third-party Markdown is not ours to gate.
        dirnames[:] = [
            d for d in dirnames if not d.startswith(".") and d not in ("node_modules", "venv")
        ]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            base = os.path.dirname(path)
            for match in LINK_RE.finditer(text):
                target = match.group(1).strip()
                if target.startswith(SKIP_PREFIXES):
                    continue
                rel = target.split()[0].split("#", 1)[0]
                if not rel:
                    continue
                total += 1
                resolved = os.path.normpath(os.path.join(base, rel))
                if not os.path.exists(resolved):
                    broken.append((path, target))

    print(f"Checked {total} relative Markdown link(s).")
    if broken:
        print(f"BROKEN: {len(broken)}")
        for src, target in sorted(broken):
            print(f"  {src} -> {target}")
        return 1
    print("All relative links resolve.")
    return 0


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    raise SystemExit(check(root))
