from joumon_provider_contract_poc import run
from joumon_evidence_adapter import to_evidence
from joumon_evidence_verifier import verify
from joumon_human_gate import prepare_human_gate, record_human_decision


def make_input():
    c, p, results = run()
    evidence = tuple(to_evidence(c.context_id, p.protocol_id, r.runtime_id, r.output, r.metadata) for r in results)
    verification_ids = tuple(verify(e, expected_context_id=c.context_id, expected_protocol_id=p.protocol_id).evidence_id for e in evidence)
    return prepare_human_gate(gate_id="unused", context_id=c.context_id, protocol_id=p.protocol_id, evidence=evidence, verification_ids=verification_ids)


def test_human_gate_collects_comparative_evidence():
    gate = make_input()
    assert len(gate.evidence) == 2
    assert gate.decision_authority == "human"


def test_human_gate_records_explicit_human_decision():
    record = record_human_decision(make_input(), decision="accept for human-reviewed next step")
    assert record.authority == "human"
    assert record.decision.startswith("accept")


def test_empty_decision_is_rejected():
    try:
        record_human_decision(make_input(), decision=" ")
    except ValueError:
        pass
    else:
        raise AssertionError("empty human decision must be rejected")
