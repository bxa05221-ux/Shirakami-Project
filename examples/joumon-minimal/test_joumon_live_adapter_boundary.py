from joumon_live_adapter_boundary import LiveAdapterRequest, LiveRuntimeAdapter, adapter_contract_snapshot
from joumon_provider_contract_poc import Context, ProtocolSpec


def fake_provider(request: LiveAdapterRequest) -> str:
    return f"live-observation:{request.context_id}:{request.protocol_id}"


def test_live_adapter_keeps_provider_outside_protocol():
    c = Context("live-001", "observe", ("human review",))
    p = ProtocolSpec("live-protocol-001", c.context_id)
    adapter = LiveRuntimeAdapter("runtime-live", "provider-external", fake_provider)
    result = adapter.execute(c, p)
    assert result.metadata["mode"] == "live"
    assert result.metadata["provider"] == "provider-external"
    assert result.context_id == c.context_id


def test_live_adapter_contract_is_provider_neutral():
    c = Context("live-002", "observe", ())
    p = ProtocolSpec("live-protocol-002", c.context_id)
    adapter = LiveRuntimeAdapter("runtime-live", "provider-external", fake_provider)
    snapshot = adapter_contract_snapshot(c, p, adapter)
    assert snapshot["context_id"] == c.context_id
    assert snapshot["protocol_id"] == p.protocol_id
    assert snapshot["mode"] == "live"
