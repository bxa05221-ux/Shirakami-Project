from joumon_matome_pipeline import run_from_matome
from joumon_live_adapter_boundary import LiveAdapterRequest


def provider_a(request: LiveAdapterRequest) -> str:
    return f"A observed: {request.prompt}"


def provider_b(request: LiveAdapterRequest) -> str:
    return f"B observed: {request.prompt}"


def document():
    return {
        "matome": {"codename": "JOUMON", "version": "0.1", "statement": "Observe a shared task."},
        "purpose": {"primary": ["preserve context"]},
        "human_gate": {"input": ["Evidence", "Verification"]},
    }


def test_matome_drives_multiple_runtime_observations():
    context, protocol, observations = run_from_matome(document(), [
        ("runtime-a", "provider-a", provider_a),
        ("runtime-b", "provider-b", provider_b),
    ])
    assert context.context_id.startswith("matome:0.1:JOUMON")
    assert protocol.context_id == context.context_id
    assert len(observations) == 2
    e1, l1 = observations[0]
    e2, l2 = observations[1]
    assert e1.context_id == e2.context_id == context.context_id
    assert e1.protocol_id == e2.protocol_id == protocol.protocol_id
    assert e1.provider != e2.provider
    assert l1.evidence_id == e1.evidence_id
    assert l2.evidence_id == e2.evidence_id
