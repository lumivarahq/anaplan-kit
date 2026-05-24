"""Command-line interface for the offline modeling tools.

Subcommands::

    anaplan-model scaffold feature "Headcount Bonus"
    anaplan-model scaffold module "Revenue" --disco CALC --dims "A,B" \\
        --line-items "Revenue:Number:Sum,Price:Number:None"
    anaplan-model lint path/to/blueprint.md
    anaplan-model size --dims "L3 Cost Centre=500,Time=36,Versions=3" --line-items 20

Everything is local — no Anaplan tenant is contacted.
"""

from __future__ import annotations

import argparse
import sys

from .blueprint import parse_blueprint
from .lint import has_errors, lint_module
from .model import Disco, LineItem
from .scaffold import scaffold_feature, scaffold_module
from .sizing import cell_count, DEFAULT_THRESHOLD


def _parse_dims_csv(text: str) -> list[str]:
    """Parse ``"A,B,C"`` into ``["A", "B", "C"]`` (for scaffold --dims)."""
    return [d.strip() for d in (text or "").split(",") if d.strip()]


def _parse_sized_dims(text: str) -> dict[str, int]:
    """Parse ``"L3 Cost Centre=500,Time=36"`` into ``{name: size}``."""
    sizes: dict[str, int] = {}
    for pair in (text or "").split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise ValueError(f"bad --dims entry '{pair}' (expected NAME=SIZE)")
        name, _, value = pair.partition("=")
        sizes[name.strip()] = int(value.strip())
    return sizes


def _parse_line_items_csv(text: str | None) -> list[LineItem] | None:
    """Parse ``"Revenue:Number:Sum,Price:Number:None"`` into line items.

    Each entry is ``Name:Format:Summary`` (Summary "None" → no summary set).
    """
    if not text:
        return None
    items: list[LineItem] = []
    for entry in text.split(","):
        entry = entry.strip()
        if not entry:
            continue
        parts = [p.strip() for p in entry.split(":")]
        name = parts[0] if len(parts) > 0 else ""
        fmt = parts[1] if len(parts) > 1 else "Number"
        summary_raw = parts[2] if len(parts) > 2 else "Sum"
        summary: str | None = None if summary_raw.lower() in ("none", "") else summary_raw
        items.append(LineItem(name=name, format=fmt, summary=summary))
    return items


def _cmd_scaffold(args: argparse.Namespace) -> int:
    if args.kind == "feature":
        files = scaffold_feature(args.name)
        for filename, content in files.items():
            print(f"===== {filename} =====")
            print(content)
            print()
        return 0
    # module
    disco = Disco[args.disco.upper()]
    dims = _parse_dims_csv(args.dims) if args.dims else []
    line_items = _parse_line_items_csv(args.line_items)
    print(scaffold_module(args.name, disco, dims, line_items))
    return 0


def _cmd_lint(args: argparse.Namespace) -> int:
    try:
        with open(args.path, "r", encoding="utf-8") as fh:
            md = fh.read()
    except OSError as exc:
        print(f"ERROR: cannot read {args.path}: {exc}", file=sys.stderr)
        return 2

    modules = parse_blueprint(md)
    findings = []
    for m in modules:
        findings.extend(lint_module(m))

    if not findings:
        print(f"OK — parsed {len(modules)} module(s), no findings.")
        return 0

    counts = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for f in findings:
        counts[f.severity] += 1
        print(str(f))
    print(
        f"\n{len(modules)} module(s); "
        f"{counts['ERROR']} error(s), {counts['WARN']} warning(s), "
        f"{counts['INFO']} info."
    )
    return 1 if has_errors(findings) else 0


def _cmd_size(args: argparse.Namespace) -> int:
    sizes = _parse_sized_dims(args.dims)
    count = cell_count(sizes, args.line_items)
    dims_desc = " × ".join(f"{k}({v})" for k, v in sizes.items()) or "(no dimensions)"
    print(f"{dims_desc} × {args.line_items} line item(s) = {count:,} cells")
    if count > args.threshold:
        print(
            f"WARN LARGE_MODULE: estimated {count:,} cells exceeds threshold "
            f"{args.threshold:,} — consider trimming Applies To or splitting "
            f"Inputs from Calculations (Performance)"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="anaplan-model",
        description="Offline Anaplan modeling tools (scaffold / lint / size). "
        "No tenant or network required.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # scaffold
    p_scaffold = sub.add_parser("scaffold", help="generate skeleton blueprints")
    scaffold_sub = p_scaffold.add_subparsers(dest="kind", required=True)

    p_feat = scaffold_sub.add_parser("feature", help="a full DISCO skeleton set")
    p_feat.add_argument("name", help="feature name, e.g. \"Headcount Bonus\"")
    p_feat.set_defaults(func=_cmd_scaffold)

    p_mod = scaffold_sub.add_parser("module", help="a single module skeleton")
    p_mod.add_argument("name", help="module name, e.g. \"CAL01 Revenue\"")
    p_mod.add_argument(
        "--disco", required=True,
        choices=[d.name for d in Disco],
        help="DISCO type (DATA/INPUTS/SYSTEM/CALC/OUTPUTS)",
    )
    p_mod.add_argument("--dims", default="", help="comma-separated dimensions, e.g. \"A,B\"")
    p_mod.add_argument(
        "--line-items", default=None,
        help="comma-separated Name:Format:Summary, e.g. "
        "\"Revenue:Number:Sum,Price:Number:None\"",
    )
    p_mod.set_defaults(func=_cmd_scaffold)

    # lint
    p_lint = sub.add_parser("lint", help="parse a blueprint .md and lint it")
    p_lint.add_argument("path", help="path to a blueprint Markdown file")
    p_lint.set_defaults(func=_cmd_lint)

    # size
    p_size = sub.add_parser("size", help="estimate a module's cell count")
    p_size.add_argument(
        "--dims", required=True,
        help="comma-separated NAME=SIZE, e.g. \"L3 Cost Centre=500,Time=36\"",
    )
    p_size.add_argument("--line-items", type=int, required=True, help="number of line items")
    p_size.add_argument(
        "--threshold", type=int, default=DEFAULT_THRESHOLD,
        help=f"warn above this cell count (default {DEFAULT_THRESHOLD:,})",
    )
    p_size.set_defaults(func=_cmd_size)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
