"""Minimal stdlib HTTP transport for the provider-neutral Shirakami API."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Mapping
from urllib.parse import urlparse

from runtime.api import ShirakamiAPI


class ShirakamiHTTPHandler(BaseHTTPRequestHandler):
    api: ShirakamiAPI

    def _json(self, status: int, payload: Mapping[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self._json(200, {"status": "ok", "service": "shirakami-api"})
            return
        if path == "/v1/capabilities":
            self._json(200, {"capabilities": self.api.capabilities})
            return
        if path.startswith("/v1/semantic-handoff/"):
            status, payload = self.api.get(
                path,
                project="http-api",
                objective="semantic-handoff retrieval",
                protocol_ids=[],
                verification_scope="transport",
            )
            self._json(status, payload)
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        self._json(405, {
            "error": "method_not_allowed",
            "authority": "human_gate_required",
        })

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(
    traces: Mapping[str, Mapping[str, Any]],
    host: str = "127.0.0.1",
    port: int = 8787,
) -> None:
    api = ShirakamiAPI(traces)
    ShirakamiHTTPHandler.api = api
    server = ThreadingHTTPServer((host, port), ShirakamiHTTPHandler)
    print(f"Shirakami API: http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    serve({})
