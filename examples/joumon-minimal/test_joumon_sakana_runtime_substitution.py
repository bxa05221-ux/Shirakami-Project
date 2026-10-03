from joumon_sakana_runtime_substitution import run_substitution_experiment


def test_runtime_substitution_preserves_semantic_and_authority_boundary():
    context, protocol, observations = run_substitution_experiment()
    (fugu_evidence, fugu_lineage), (alternate_evidence, alternate_lineage) = observations

    # Semantic identity remains invariant.
    assert fugu_evidence.context_id == alternate_evidence.context_id == context.context_id
    assert fugu_evidence.protocol_id == alternate_evidence.protocol_id == protocol.protocol_id

    # Runtime identity and provenance are allowed to change.
    assert fugu_evidence.runtime_id != alternate_evidence.runtime_id
    assert fugu_evidence.metadata["provider"] != alternate_evidence.metadata["provider"]

    # Human authority remains outside the runtime.
    assert context.final_decision_authority == "human"
    assert protocol.human_gate_required is True

    # Lineage follows the evidence produced by each runtime.
    assert fugu_lineage.evidence_id == fugu_evidence.evidence_id
    assert alternate_lineage.evidence_id == alternate_evidence.evidence_id
