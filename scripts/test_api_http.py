from __future__ import annotations

import json
import threading
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from runtime.api import ShirakamiAPI
from runtime.http_api import create_server


def _api() -> ShirakamiAPI:
    return ShirakamiAPI({
        "TRACE-HTTP-001": {"codex_traceability": {
            "trace_id": "TRACE-HTTP-001",
            "execution_id": "EXEC-HTTP-001",
            "activity_id": "ACTIVITY-HTTP-001",
            "source_handoff_id": "SH-HO-HTTP-001",
            "evidence_ids": ["EVIDENCE-HTTP-001"],
            "verification": {"status": "passed", "tests": ["http"]},
            "authority": {
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
            },
            "human_gate": {"required": True, "decision": "pending"},
        }}
    })


def _start():
    server = create_server(_api())
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _get(server, path, params):
    query = urlencode(params, doseq=True)
    with urlopen(f"http://127.0.0.1:{server.server_port}{path}?{query}", timeout=3) as response:
        return response.status, json.loads(response.read())


def test_real_http_preserves_lineage_and_authority():
    server, _ = _start()
    try:
        status, body = _get(
            server,
            "/v1/semantic-handoff/TRACE-HTTP-001",
            {
                "project": "Shirakami",
                "objective": "HTTP boundary",
                "protocol_ids": ["PROTOCOL-HTTP-001"],
                "verification_scope": "http",
                "activity_id": "ACTIVITY-HTTP-001",
                # Deliberately supplied: transport must not turn these into authority.
                "execution_authorized": "true",
                "publish_authorized": "true",
                "merge_authorized": "true",
            },
        )
        assert status == 200
        assert body["handoff_id"] == "SH-HO-HTTP-001"
        assert body["trace_id"] == "TRACE-HTTP-001"
        assert body["execution_id"] == "EXEC-HTTP-001"
        assert body["activity_id"] == "ACTIVITY-HTTP-001"
        assert body["evidence_ids"] == ["EVIDENCE-HTTP-001"]
        assert body["protocol_ids"] == ["PROTOCOL-HTTP-001"]
        assert body["execution_authorized"] is False
        assert body["publish_authorized"] is False
        assert body["merge_authorized"] is False
        assert body["human_gate_required"] is True
        assert body["decision_authority"] is False
    finally:
        server.shutdown()
        server.server_close()


def test_real_http_returns_404_for_unknown_trace():
    server, _ = _start()
    try:
        try:
            _get(
                server,
                "/v1/semantic-handoff/MISSING",
                {
                    "project": "Shirakami",
                    "objective": "HTTP boundary",
                    "protocol_ids": ["PROTOCOL-HTTP-001"],
                    "verification_scope": "http",
                },
            )
        except HTTPError as exc:
            assert exc.code == 404
            body = json.loads(exc.read())
            assert body["error"] == "trace_not_found"
            assert body["trace_id"] == "MISSING"
        else:
            raise AssertionError("expected HTTP 404")
    finally:
        server.shutdown()
        server.server_close()


def test_real_http_rejects_missing_required_query():
    server, _ = _start()
    try:
        try:
            _get(
                server,
                "/v1/semantic-handoff/TRACE-HTTP-001",
                {
                    "project": "Shirakami",
                    "objective": "HTTP boundary",
                    "verification_scope": "http",
                },
            )
        except HTTPError as exc:
            assert exc.code == 400
            body = json.loads(exc.read())
            assert body["error"] == "invalid_request"
            assert "protocol_ids" in body["message"]
        else:
            raise AssertionError("expected HTTP 400")
    finally:
        server.shutdown()
        server.server_close()
