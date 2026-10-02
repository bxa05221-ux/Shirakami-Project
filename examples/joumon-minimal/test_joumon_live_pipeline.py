from joumon_live_adapter_boundary import LiveAdapterRequest
from joumon_live_pipeline import run_live_observation
from joumon_provider_contract_poc import Context, ProtocolSpec


def provider_one(request: LiveAdapterRequest) -> str:
    return f"provider-one observation for {request.context_id}"


def provider_two(request: LiveAdapterRequest) -> str:
    return f"provider-two observation for {request.context_id}"


def test_two_provider_adapters_share_same_evidence_boundary():
    c = Context("live-pipeline-001", "observe", ("human review",))
    p = ProtocolSpec("live-pipeline-protocol-001", c.context_id)
    e1, l1 = run_live_observation(context=c, protocol=p, runtime_id="runtime-one", provider="provider-one", invoke=provider_one)
    e2, l2 = run_live_observation(context=c, protocol=p, runtime_id="runtime-two", provider="provider-two", invoke=provider_two)
    assert e1.context_id == e2.context_id == c.context_id
    assert e1.protocol_id == e2.protocol_id == p.protocol_id
    assert e1.provider != e2.provider
    assert l1.evidence_id == e1.evidence_id
    assert l2.evidence_id == e2.evidence_id
    assert e1.evidence_id != e2.evidence_id
