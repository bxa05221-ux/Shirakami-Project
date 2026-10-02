from joumon_provider_contract_poc import run
from joumon_evidence_adapter import to_evidence
from joumon_lineage import build_lineage
from joumon_semantic_handoff import create_handoff
from joumon_matome_yaml import handoff_to_matome_yaml, validate_matome_document


def make_handoff():
    c, p, results = run()
    evidence = tuple(to_evidence(c.context_id, p.protocol_id, r.runtime_id, r.output, r.metadata) for r in results)
    lineage = tuple(build_lineage(context_id=c.context_id, protocol_id=p.protocol_id, runtime_id=e.runtime_id, evidence_id=e.evidence_id) for e in evidence)
    return create_handoff(handoff_id="matome-001", context_id=c.context_id, protocol_id=p.protocol_id, evidence=evidence, lineage=lineage)


def test_handoff_serializes_to_matome_shape():
    payload = validate_matome_document(handoff_to_matome_yaml(make_handoff()))
    assert payload["matome_version"] == "joumon-0.1"
    assert len(payload["evidence"]) == 2
    assert len(payload["lineage"]) == 2


def test_matome_bridge_preserves_human_authority():
    payload = validate_matome_document(handoff_to_matome_yaml(make_handoff()))
    assert payload["authority"]["handoff"] == "non-authoritative"
    assert payload["authority"]["final_decision"] == "human"


def test_invalid_authority_is_rejected():
    document = handoff_to_matome_yaml(make_handoff()).replace('"final_decision": "human"', '"final_decision": "runtime"')
    try:
        validate_matome_document(document)
    except ValueError:
        pass
    else:
        raise AssertionError("authority escalation must be rejected")
