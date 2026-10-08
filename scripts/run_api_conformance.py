"""Run the fixed Shirakami API v1.0 transport gate."""
from __future__ import annotations

import subprocess
import sys

API_TESTS = [
    "scripts/test_api_semantic_handoff.py",
    "scripts/test_api_semantic_handoff_e2e.py",
    "scripts/test_validate_api_boundary.py",
    "scripts/test_api_http.py",
]


def main() -> int:
    cmd = [sys.executable, "-m", "pytest", "-q", *API_TESTS]
    print("SHIRAKAMI API v1.0 CONFORMANCE")
    print("tests:", len(API_TESTS))
    print("principle: real HTTP transport does not create authority")
    print("principle: lineage survives the HTTP boundary")
    print("scope: fixed API v1.0 gate; no expanded permutation suite")
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
