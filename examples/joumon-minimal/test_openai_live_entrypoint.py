import os
import pytest
from openai_live_entrypoint import require_live_config


def test_live_entrypoint_requires_explicit_configuration(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    with pytest.raises(RuntimeError):
        require_live_config()


def test_live_entrypoint_requires_explicit_model(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-placeholder")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    with pytest.raises(RuntimeError):
        require_live_config()
