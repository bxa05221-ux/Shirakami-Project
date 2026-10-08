"""Minimal external-client example for Shirakami API v1.0."""
from __future__ import annotations

import json
import sys
from urllib.parse import urlencode
from urllib.request import urlopen


def fetch_handoff(base_url: str, trace_id: str) -> dict:
    query = urlencode({
        "project": "Shirakami",
        "objective": "external client demonstration",
        "protocol_ids": ["PROTOCOL-EXAMPLE-001"],
        "verification_scope": "api-v1",
    }, doseq=True)
    with urlopen(
        f"{base_url.rstrip('/')}/v1/semantic-handoff/{trace_id}?{query}",
        timeout=5,
    ) as response:
        return json.loads(response.read())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python examples/api-v1-client.py BASE_URL TRACE_ID")
    print(json.dumps(fetch_handoff(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=2))
