from joumon_live_adapter_boundary import LiveAdapterRequest
from joumon_openai_adapter import build_openai_compatible_adapter
from joumon_provider_contract_poc import Context, ProtocolSpec


def fake_openai(request: LiveAdapterRequest, model: str) -> str:
    return f"{model}: observation for {request.context_id}"


def test_openai_compatible_adapter_is_provider_boundary_only():
    context = Context("openai-boundary-001", "observe", ("human review",))
    protocol = ProtocolSpec("openai-boundary-protocol-001", context.context_id)
    adapter = build_openai_compatible_adapter(model="test-model", invoke=fake_openai)
    result = adapter.execute(context, protocol)
    assert result.metadata["provider"] == "openai-compatible"
    assert result.metadata["mode"] == "live"
    assert "test-model" in result.output
    assert result.context_id == context.context_id
