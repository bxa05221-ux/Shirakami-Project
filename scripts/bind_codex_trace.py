#!/usr/bin/env python3
"""Bind an observed Git commit to an existing pending Codex trace."""

from __future__ import annotations

import argparse
from pathlib import Path
import yaml


def bind(trace: dict, commit: str, changed_paths: list[str]) -> dict:
    root = trace.get("codex_traceability")
    if not isinstance(root, dict):
        raise ValueError("missing codex_traceability")
    if not root.get("source_handoff_id"):
        raise ValueError("source_handoff_id is required")
    if not commit:
        raise ValueError("commit is required")
    if not isinstance(changed_paths, list):
        raise ValueError("changed_paths must be a list")

    root["commit"] = commit
    root["result"]["changed_paths"] = changed_paths
    return trace


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    trace = yaml.safe_load(args.trace.read_text(encoding="utf-8"))
    bound = bind(trace or {}, args.commit, args.changed_path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(bound, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Bound observed commit to trace: {args.commit}")
    print("Commit binding does not grant execution, publish, or merge authority.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
