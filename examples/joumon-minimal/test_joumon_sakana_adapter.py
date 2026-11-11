from joumon_live_adapter_boundary import LiveAdapterRequest
from joumon_sakana_adapter import build_sakana_fugu_adapter
from joumon_provider_contract_poc import Context, ProtocolSpec


def fake_fugu(request: LiveAdapterRequest, model: str) -> str:
    return f"{model}: observation for {request.context_id}"


def test_sakana_fugu_is_a_replaceable_runtime_boundary():
    context = Context("sakana-boundary-001", "observe", ("human review",))
    protocol = ProtocolSpec("sakana-boundary-protocol-001", context.context_id)
    adapter = build_sakana_fugu_adapter(invoke=fake_fugu)
    result = adapter.execute(context, protocol)

    assert result.metadata["provider"] == "sakana-ai"
    assert result.metadata["mode"] == "live"
    assert result.metadata["runtime_type"] == "model"
    assert "fugu" in result.output
    assert result.context_id == context.context_id


def test_sakana_runtime_keeps_protocol_identity_outside_provider_name():
    context = Context("sakana-boundary-002", "compare", ("evidence",))
    protocol = ProtocolSpec("sakana-boundary-protocol-002", context.context_id)
    adapter = build_sakana_fugu_adapter(model="fugu-ultra", invoke=fake_fugu)

    result = adapter.execute(context, protocol)

    assert result.context_id == context.context_id
    assert result.metadata["provider"] == "sakana-ai"
    assert result.metadata["mode"] == "live"
