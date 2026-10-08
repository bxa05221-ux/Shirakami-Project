"""Minimal local server for the Shirakami API v1.0 external-developer demo."""
from __future__ import annotations

from runtime.api import ShirakamiAPI
from runtime.http_api import create_server

TRACES = {
    "TRACE-HTTP-001": {
        "codex_traceability": {
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
        }
    }
}

if __name__ == "__main__":
    server = create_server(ShirakamiAPI(TRACES), host="127.0.0.1", port=8000)
    print("Shirakami API v1.0 demo: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
