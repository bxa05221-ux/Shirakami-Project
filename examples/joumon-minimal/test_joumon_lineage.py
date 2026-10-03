from joumon_provider_contract_poc import run
from joumon_evidence_adapter import to_evidence
from joumon_lineage import build_lineage


def test_lineage_connects_context_protocol_runtime_and_evidence():
    context, protocol, results = run()
    evidence = to_evidence(context.context_id, protocol.protocol_id, results[0].runtime_id, results[0].output, results[0].metadata)
    lineage = build_lineage(context_id=context.context_id, protocol_id=protocol.protocol_id, runtime_id=evidence.runtime_id, evidence_id=evidence.evidence_id)
    assert {n.node_type for n in lineage.nodes} == {"context", "protocol", "runtime", "evidence"}
    assert len(lineage.edges) == 3


def test_lineage_preserves_provenance_path():
    context, protocol, results = run()
    evidence = to_evidence(context.context_id, protocol.protocol_id, results[0].runtime_id, results[0].output, results[0].metadata)
    lineage = build_lineage(context_id=context.context_id, protocol_id=protocol.protocol_id, runtime_id=evidence.runtime_id, evidence_id=evidence.evidence_id)
    relations = {(e.source_id, e.relation, e.target_id) for e in lineage.edges}
    assert (context.context_id, "bound-by", protocol.protocol_id) in relations
    assert (protocol.protocol_id, "executed-by", evidence.runtime_id) in relations
    assert (evidence.runtime_id, "produced-observation", evidence.evidence_id) in relations


def test_lineage_has_no_decision_authority():
    context, protocol, results = run()
    evidence = to_evidence(context.context_id, protocol.protocol_id, results[0].runtime_id, results[0].output, results[0].metadata)
    assert build_lineage(context_id=context.context_id, protocol_id=protocol.protocol_id, runtime_id=evidence.runtime_id, evidence_id=evidence.evidence_id).authority == "non-authoritative"
