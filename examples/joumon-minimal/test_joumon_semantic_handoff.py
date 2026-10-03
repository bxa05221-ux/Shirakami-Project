from joumon_provider_contract_poc import run
from joumon_evidence_adapter import to_evidence
from joumon_lineage import build_lineage
from joumon_semantic_handoff import create_handoff


def make():
    context, protocol, results = run()
    evidence = tuple(to_evidence(context.context_id, protocol.protocol_id, r.runtime_id, r.output, r.metadata) for r in results)
    lineage = tuple(build_lineage(context_id=context.context_id, protocol_id=protocol.protocol_id, runtime_id=e.runtime_id, evidence_id=e.evidence_id) for e in evidence)
    return context, protocol, evidence, lineage


def test_handoff_preserves_context_protocol_evidence_and_lineage():
    c, p, evidence, lineage = make()
    h = create_handoff(handoff_id="handoff-001", context_id=c.context_id, protocol_id=p.protocol_id, evidence=evidence, lineage=lineage)
    assert h.context_id == c.context_id
    assert h.protocol_id == p.protocol_id
    assert len(h.evidence) == len(evidence)
    assert len(h.lineage) == len(lineage)


def test_handoff_rejects_mismatched_evidence():
    c, p, evidence, lineage = make()
    bad = evidence[0].__class__(evidence[0].evidence_id, "wrong-context", evidence[0].protocol_id, evidence[0].runtime_id, evidence[0].provider, evidence[0].runtime_type, evidence[0].mode, evidence[0].observed_output)
    try:
        create_handoff(handoff_id="handoff-bad", context_id=c.context_id, protocol_id=p.protocol_id, evidence=(bad,), lineage=())
    except ValueError:
        pass
    else:
        raise AssertionError("mismatched Evidence must be rejected")


def test_handoff_rejects_unrelated_lineage():
    c, p, evidence, lineage = make()
    try:
        create_handoff(handoff_id="handoff-bad-lineage", context_id=c.context_id, protocol_id=p.protocol_id, evidence=evidence, lineage=(build_lineage(context_id=c.context_id, protocol_id=p.protocol_id, runtime_id="other", evidence_id="other-evidence"),))
    except ValueError:
        pass
    else:
        raise AssertionError("unrelated Lineage must be rejected")


def test_handoff_has_no_authority_transfer():
    c, p, evidence, lineage = make()
    h = create_handoff(handoff_id="handoff-002", context_id=c.context_id, protocol_id=p.protocol_id, evidence=evidence, lineage=lineage)
    assert h.authority == "non-authoritative"
    assert h.final_decision_authority == "human"
