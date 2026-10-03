from joumon_handoff_chain import run_chain


def test_chain_preserves_context_and_protocol_across_handoff():
    context, protocol, handoff, second, _ = run_chain()
    assert handoff.context_id == context.context_id
    assert handoff.protocol_id == protocol.protocol_id
    assert second.context_id == context.context_id


def test_chain_preserves_prior_evidence_and_adds_new_observation():
    _, _, handoff, second, lineage = run_chain()
    assert len(handoff.evidence) == 1
    assert handoff.evidence[0].runtime_id == "runtime-a"
    assert second.runtime_id == "runtime-b"
    assert lineage.evidence_id == second.evidence_id


def test_chain_keeps_runtime_provenance_separate():
    _, _, handoff, second, _ = run_chain()
    assert handoff.evidence[0].provider == "provider-a"
    assert second.provider == "provider-b"


def test_chain_does_not_transfer_authority():
    context, _, handoff, second, _ = run_chain()
    assert context.final_decision_authority == "human"
    assert handoff.final_decision_authority == "human"
    assert second.final_decision_authority == "human"
