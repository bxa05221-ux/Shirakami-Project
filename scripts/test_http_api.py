import json
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from threading import Thread

from api.http_server import ShirakamiHTTPHandler


def _server():
    ShirakamiHTTPHandler.api = type(
        "API", (), {
            "capabilities": {
                "semantic_handoff": True,
                "candidate_creation": True,
                "human_gate": False,
                "state_snapshot": True,
            },
        }
    )()
    server = ThreadingHTTPServer(("127.0.0.1", 0), ShirakamiHTTPHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def test_health_and_capabilities():
    server, thread = _server()
    try:
        connection = HTTPConnection("127.0.0.1", server.server_port)
        connection.request("GET", "/health")
        response = connection.getresponse()
        assert response.status == 200
        assert json.loads(response.read())["status"] == "ok"

        connection.request("GET", "/v1/capabilities")
        response = connection.getresponse()
        assert response.status == 200
        capabilities = json.loads(response.read())["capabilities"]
        assert capabilities["candidate_creation"] is True
        assert capabilities["human_gate"] is False

        connection.request("GET", "/v1/state")
        response = connection.getresponse()
        assert response.status == 200
        assert json.loads(response.read())["state"] == {}

        connection.request("POST", "/v1/human-gate")
        response = connection.getresponse()
        assert response.status == 405
        assert json.loads(response.read())["authority"] == "human_gate_required"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
