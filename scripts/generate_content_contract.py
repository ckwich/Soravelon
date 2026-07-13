#!/usr/bin/env python
"""Generate or check Soravelon's versioned offline content contract."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from world.content_contract import DEFAULT_ARTIFACT_PATH, render_content_contract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_ARTIFACT_PATH)
    options = parser.parse_args()
    rendered = render_content_contract()
    if options.check:
        if not options.output.exists() or options.output.read_text() != rendered:
            print(f"Content contract is stale: {options.output}", file=sys.stderr)
            return 1
        print(f"Content contract is current: {options.output}")
        return 0
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(rendered)
    print(f"Wrote content contract: {options.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
