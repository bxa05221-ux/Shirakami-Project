from joumon_roundtrip_runtime import execute_roundtrip


def test_runtime_b_consumes_restored_handoff():
    restored, evidence, lineage = execute_roundtrip()
    assert restored.context_id == evidence.context_id
    assert restored.protocol_id == evidence.protocol_id
    assert restored.evidence[0].runtime_id == "runtime-a"
    assert evidence.runtime_id == "runtime-b"
    assert lineage.evidence_id == evidence.evidence_id


def test_end_to_end_preserves_cross_runtime_provenance():
    restored, evidence, _ = execute_roundtrip()
    assert restored.evidence[0].provider == "provider-a"
    assert evidence.provider == "provider-b"
    assert restored.evidence[0].evidence_id != evidence.evidence_id


def test_end_to_end_keeps_human_authority():
    restored, _, _ = execute_roundtrip()
    assert restored.authority == "non-authoritative"
    assert restored.final_decision_authority == "human"
