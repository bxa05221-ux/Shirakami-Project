from __future__ import annotations

import json
import threading
from urllib.error import HTTPError
from urllib.request import urlopen

from runtime.human_gate_http_api import create_server


def _get(server, path):
    with urlopen(f"http://127.0.0.1:{server.server_port}{path}", timeout=3) as response:
        return response.status, json.loads(response.read())


def test_profile_endpoint_exposes_review_configuration_without_authority():
    server = create_server()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        status, body = _get(server, "/v1/human-gate/profiles/strategic")
        profile = body["human_gate_profile"]
        assert status == 200
        assert profile["id"] == "strategic"
        assert profile["authority"]["ai"]["may_generate_options"] is True
        assert profile["authority"]["ai"]["may_select_strategy"] is False
        assert profile["authority"]["ai"]["may_rank_options"] is False
        assert profile["authority"]["ai"]["may_commit_decision"] is False
        assert profile["authority"]["human_gate"]["may_select_strategy"] is True
        assert profile["invariants"]["selection_authority"] == "human_gate"
        assert profile["invariants"]["human_gate_required"] is True
    finally:
        server.shutdown()
        server.server_close()


def test_profile_endpoint_returns_404_for_unknown_profile():
    server = create_server()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        try:
            _get(server, "/v1/human-gate/profiles/unknown")
        except HTTPError as exc:
            assert exc.code == 404
            body = json.loads(exc.read())
            assert body["error"] == "profile_not_found"
        else:
            raise AssertionError("expected HTTP 404")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    test_profile_endpoint_exposes_review_configuration_without_authority()
    test_profile_endpoint_returns_404_for_unknown_profile()
    print("Strategic Human Gate API tests: 2 passed")
