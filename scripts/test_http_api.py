import json
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from threading import Thread

from api.http_server import ShirakamiHTTPHandler


def test_health_and_capabilities():
    ShirakamiHTTPHandler.api = type(
        "API",
        (),
        {"capabilities": {"semantic_handoff": True}},
    )()
    server = ThreadingHTTPServer(("127.0.0.1", 0), ShirakamiHTTPHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        connection = HTTPConnection("127.0.0.1", server.server_port)
        connection.request("GET", "/health")
        response = connection.getresponse()
        assert response.status == 200
        assert json.loads(response.read())["status"] == "ok"

        connection.request("GET", "/v1/capabilities")
        response = connection.getresponse()
        assert response.status == 200
        assert json.loads(response.read())["capabilities"]["semantic_handoff"] is True

        connection.request("POST", "/v1/human-gate")
        response = connection.getresponse()
        assert response.status == 405
        assert json.loads(response.read())["authority"] == "human_gate_required"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
