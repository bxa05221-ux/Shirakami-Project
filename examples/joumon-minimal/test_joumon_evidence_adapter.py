from joumon_provider_contract_poc import run
from joumon_evidence_adapter import to_evidence

def records():
    context, protocol, results = run()
    return tuple(to_evidence(context.context_id, protocol.protocol_id, r.runtime_id, r.output, r.metadata) for r in results)

def test_different_provider_results_share_one_evidence_shape():
    assert len({type(r) for r in records()}) == 1
    assert {r.provider for r in records()} == {"openai", "gemini"}

def test_evidence_retains_context_and_protocol_identity():
    rs=records()
    assert all(r.context_id == "joumon-provider-contract-001" for r in rs)
    assert all(r.protocol_id == "joumon-provider-contract-001" for r in rs)

def test_provider_metadata_does_not_change_authority():
    assert all(r.evidence_authority == "non-authoritative" and r.final_decision_authority == "human" for r in records())

def test_mock_mode_is_explicit():
    assert all(r.mode == "mock" for r in records())

def test_provider_identity_stays_outside_context():
    context, _, _ = run()
    assert context.final_decision_authority == "human"
    assert not hasattr(context, "provider")
