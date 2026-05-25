"""Offline cell-count estimation for modules.

A module's cell count is the product of its dimension sizes times the number of
line items. This is the single most useful back-of-envelope number when
designing for *Performance* — it tells you, before you build, whether a module
will be tens of thousands of cells or hundreds of millions.
"""

from __future__ import annotations

from .model import Finding, Module

DEFAULT_THRESHOLD = 10_000_000


def cell_count(dimension_sizes: dict[str, int], line_items: int) -> int:
    """Cells = product(dimension sizes) x line_items.

    An empty ``dimension_sizes`` means the module is dimensionless (one cell per
    line item), so the result is just ``line_items``.
    """
    product = 1
    for size in dimension_sizes.values():
        product *= int(size)
    if not dimension_sizes:
        product = 1
    return product * int(line_items)


def estimate_module(m: Module, dimension_sizes: dict[str, int]) -> int:
    """Estimate cells for ``m`` using the union of its line items' Applies To.

    Only dimensions that some line item actually uses are counted (and only
    those for which a size is supplied). Line items that share a narrower grain
    don't inflate the estimate beyond the union.
    """
    used: set[str] = set()
    for li in m.line_items:
        for dim in li.applies_to:
            used.add(dim)
    sizes = {d: s for d, s in dimension_sizes.items() if d in used}
    return cell_count(sizes, len(m.line_items))


def size_report(
    m: Module,
    dimension_sizes: dict[str, int],
    threshold: int = DEFAULT_THRESHOLD,
) -> tuple[int, list[Finding]]:
    """Return ``(cell_count, findings)`` for a module, warning if over threshold."""
    count = estimate_module(m, dimension_sizes)
    findings: list[Finding] = []
    if count > threshold:
        findings.append(
            Finding(
                "WARN",
                "LARGE_MODULE",
                f"estimated {count:,} cells exceeds threshold {threshold:,} — "
                "consider trimming Applies To or splitting Inputs from Calculations "
                "(Performance)",
                m.name,
            )
        )
    return count, findings
