from runtime.observation_evidence_validation import validate_evidence_candidate
from runtime.validated_evidence_record import build_evidence_record_from_validated
from runtime.observation_evidence_candidate import EvidenceCandidate


def validated():
    candidate = EvidenceCandidate(
        candidate_id="candidate-01",
        observation_id="observation-01",
        witness_id="witness-01",
        trace_id="trace-01",
        approval_id="approval-01",
        protocol_id="protocol-01",
        request_id="request-01",
        source="aiwitness",
        execution_status="completed",
        scope=("bounded-observation",),
    )
    return validate_evidence_candidate(candidate)


def test_validated_candidate_becomes_evidence_record():
    record = build_evidence_record_from_validated(
        validated(), observed={"value": "observed"}
    )
    assert record["evidence_id"].startswith("EVIDENCE-")
    assert record["source"]["observation_id"] == "observation-01"
    assert record["source"]["trace_id"] == "trace-01"
    assert record["authority"]["decision_authority"] is False
    assert record["authority"]["human_gate_required"] is True


def test_evidence_id_is_stable_for_same_observation():
    first = build_evidence_record_from_validated(
        validated(), observed={"value": "observed"}
    )
    second = build_evidence_record_from_validated(
        validated(), observed={"value": "observed"}
    )
    assert first["evidence_id"] == second["evidence_id"]


def test_observed_change_changes_evidence_id():
    first = build_evidence_record_from_validated(
        validated(), observed={"value": "observed"}
    )
    second = build_evidence_record_from_validated(
        validated(), observed={"value": "changed"}
    )
    assert first["evidence_id"] != second["evidence_id"]


def test_record_builder_does_not_grant_authority():
    record = build_evidence_record_from_validated(
        validated(), observed={"value": "observed"}
    )
    assert record["authority"]["execution_authorized"] is False
    assert record["authority"]["publish_authorized"] is False
    assert record["authority"]["merge_authorized"] is False
