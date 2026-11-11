import pytest
from joumon_live_fugu_entrypoint import require_config

def test_fugu_entrypoint_requires_key(monkeypatch):
    monkeypatch.delenv("SAKANA_API_KEY", raising=False)
    monkeypatch.setenv("JOUMON_STATEMENT", "test statement")
    with pytest.raises(RuntimeError, match="SAKANA_API_KEY"):
        require_config()

def test_fugu_entrypoint_requires_statement(monkeypatch):
    monkeypatch.setenv("SAKANA_API_KEY", "test-only")
    monkeypatch.delenv("JOUMON_STATEMENT", raising=False)
    with pytest.raises(RuntimeError, match="JOUMON_STATEMENT"):
        require_config()
