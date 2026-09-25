#!/usr/bin/env python3
"""Record a validated Codex result as a separate return-path artifact."""

from __future__ import annotations

import argparse
from pathlib import Path
import yaml

from validate_codex_result import validate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    payload = yaml.safe_load(args.result.read_text(encoding="utf-8"))
    errors = validate(payload or {})
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Recorded validated Codex result: {args.output}")
    print("Result does not grant execution, publish, or merge authority.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
