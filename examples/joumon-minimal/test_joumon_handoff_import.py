from joumon_provider_contract_poc import run
from joumon_evidence_adapter import to_evidence
from joumon_lineage import build_lineage
from joumon_semantic_handoff import create_handoff
from joumon_matome_yaml import handoff_to_matome_yaml, validate_matome_document
from joumon_handoff_import import matome_to_handoff


def make_document():
    c, p, results = run()
    evidence = tuple(to_evidence(c.context_id, p.protocol_id, r.runtime_id, r.output, r.metadata) for r in results)
    lineage = tuple(build_lineage(context_id=c.context_id, protocol_id=p.protocol_id, runtime_id=e.runtime_id, evidence_id=e.evidence_id) for e in evidence)
    h = create_handoff(handoff_id="roundtrip-001", context_id=c.context_id, protocol_id=p.protocol_id, evidence=evidence, lineage=lineage)
    return handoff_to_matome_yaml(h)


def test_handoff_roundtrip_preserves_identity_and_evidence():
    original = validate_matome_document(make_document())
    restored = matome_to_handoff(original)
    assert restored.handoff_id == original["handoff_id"]
    assert restored.context_id == original["context_id"]
    assert restored.protocol_id == original["protocol_id"]
    assert len(restored.evidence) == len(original["evidence"])
    assert len(restored.lineage) == len(original["lineage"])


def test_roundtrip_preserves_human_authority():
    restored = matome_to_handoff(validate_matome_document(make_document()))
    assert restored.authority == "non-authoritative"
    assert restored.final_decision_authority == "human"


def test_import_rejects_authority_escalation():
    payload = validate_matome_document(make_document())
    payload["authority"]["final_decision"] = "runtime"
    try:
        matome_to_handoff(payload)
    except ValueError:
        pass
    else:
        raise AssertionError("authority escalation must be rejected")
