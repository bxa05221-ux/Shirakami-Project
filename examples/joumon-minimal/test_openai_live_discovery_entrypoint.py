from types import SimpleNamespace

from openai_live_discovery_entrypoint import discover_model


class FakeModels:
    def __init__(self, ids):
        self.data = [SimpleNamespace(id=model_id) for model_id in ids]

    def list(self):
        return self


class FakeClient:
    def __init__(self, ids):
        self.models = FakeModels(ids)


def test_discover_model_prefers_current_general_model():
    client = FakeClient(["gpt-4o", "gpt-5", "gpt-5.6-luna"])
    assert discover_model(client) == "gpt-5.6-luna"


def test_discover_model_falls_back_to_available_gpt():
    client = FakeClient(["gpt-4o-mini", "text-embedding-3-small"])
    assert discover_model(client) == "gpt-4o-mini"


def test_discover_model_fails_without_gpt_model():
    client = FakeClient(["text-embedding-3-small"])
    try:
        discover_model(client)
    except RuntimeError as exc:
        assert "No GPT model" in str(exc)
    else:
        raise AssertionError("expected RuntimeError")
