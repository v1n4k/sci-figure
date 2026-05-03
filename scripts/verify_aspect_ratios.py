#!/usr/bin/env python3
"""verify_aspect_ratios.py — standalone CLI wrapper around
``sci_figure_lib.render.verify_aspect_ratios``.

Walks a ``.drawio`` XML, decodes each embedded PNG IHDR, and aborts if
any image cell's geometry deviates from the source PNG aspect ratio by
more than 0.5 %. Run as part of pre-export QA.

Usage:
    python verify_aspect_ratios.py <path/to/figure.drawio>
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 64
    target = Path(sys.argv[1]).expanduser().resolve()
    if not target.exists():
        print(f"[verify_aspect_ratios] not found: {target}", file=sys.stderr)
        return 1
    try:
        from sci_figure_lib.render import verify_aspect_ratios
    except ImportError as e:
        print(
            "[verify_aspect_ratios] sci_figure_lib not importable; "
            "did you run bootstrap_env.sh?",
            file=sys.stderr,
        )
        print(f"  detail: {e}", file=sys.stderr)
        return 2
    try:
        verify_aspect_ratios(target)
    except Exception as e:
        print(f"[verify_aspect_ratios] FAIL: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
