"""HTTP transport for configurable Human Gate profiles.

This is an additive extension. The fixed Semantic Handoff API v1.0 remains
unchanged; this endpoint exposes review configuration, not decisions.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from .human_gate_profile import get_profile, validate_profile


def make_handler():
    class HumanGateProfileHandler(BaseHTTPRequestHandler):
        server_version = "ShirakamiHumanGateHTTP/0.1"

        def _json(self, status: int, body: dict[str, Any]) -> None:
            payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:
            prefix = "/v1/human-gate/profiles/"
            path = urlparse(self.path).path
            if not path.startswith(prefix):
                self._json(404, {"error": "not_found"})
                return

            profile_id = path[len(prefix):]
            if not profile_id or "/" in profile_id:
                self._json(404, {"error": "not_found"})
                return

            try:
                profile = get_profile(profile_id)
                validate_profile(profile)
            except ValueError:
                self._json(404, {"error": "profile_not_found", "profile_id": profile_id})
                return

            self._json(200, {"human_gate_profile": profile})

        def log_message(self, format: str, *args: Any) -> None:
            return

    return HumanGateProfileHandler


def create_server(host: str = "127.0.0.1", port: int = 0):
    return ThreadingHTTPServer((host, port), make_handler())
