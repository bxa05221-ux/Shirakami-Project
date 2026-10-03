from types import SimpleNamespace

import openai_live_discovery_entrypoint as entrypoint


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


def test_discover_model_retries_transient_failure(monkeypatch):
    class FlakyModels:
        def __init__(self):
            self.calls = 0

        def list(self):
            self.calls += 1
            if self.calls < 3:
                raise RuntimeError("temporary 504")
            return FakeModels(["gpt-4o"])

    client = SimpleNamespace(models=FlakyModels())
    monkeypatch.setattr(entrypoint.time, "sleep", lambda _: None)

    assert discover_model(client) == "gpt-4o"
    assert client.models.calls == 3
