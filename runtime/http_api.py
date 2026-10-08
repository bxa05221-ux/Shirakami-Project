"""Minimal real HTTP transport for the provider-neutral Shirakami API boundary.

The transport is intentionally thin: it parses HTTP, delegates to ShirakamiAPI,
and serializes the already-authority-safe result. It does not add authority.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from .api import ShirakamiAPI


_REQUIRED = ("project", "objective", "protocol_ids", "verification_scope")


def _query_values(query: str) -> dict[str, list[str]]:
    return parse_qs(query, keep_blank_values=True)


def _required_query(query: dict[str, list[str]]) -> dict[str, Any]:
    missing = [name for name in _REQUIRED if not query.get(name)]
    if missing:
        raise ValueError(f"missing required query parameter(s): {', '.join(missing)}")
    return {
        "project": query["project"][0],
        "objective": query["objective"][0],
        "protocol_ids": query["protocol_ids"],
        "verification_scope": query["verification_scope"][0],
        "activity_id": query.get("activity_id", [None])[0],
    }


def make_handler(api: ShirakamiAPI):
    class ShirakamiRequestHandler(BaseHTTPRequestHandler):
        server_version = "ShirakamiHTTP/1.0"

        def _json(self, status: int, body: dict[str, Any]) -> None:
            payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if not parsed.path.startswith("/v1/semantic-handoff/"):
                self._json(404, {"error": "not_found"})
                return

            trace_id = parsed.path[len("/v1/semantic-handoff/"):]
            if not trace_id or "/" in trace_id:
                self._json(404, {"error": "not_found"})
                return

            try:
                kwargs = _required_query(_query_values(parsed.query))
                status, body = api.get(
                    f"/v1/semantic-handoff/{trace_id}",
                    **kwargs,
                )
            except ValueError as exc:
                self._json(400, {"error": "invalid_request", "message": str(exc)})
                return

            self._json(status, body)

        def log_message(self, format: str, *args: Any) -> None:
            return

    return ShirakamiRequestHandler


def create_server(api: ShirakamiAPI, host: str = "127.0.0.1", port: int = 0):
    """Create a real HTTP server; port=0 selects an available local port."""
    return ThreadingHTTPServer((host, port), make_handler(api))
