from runtime.human_approved_runtime_request import HumanApprovedProtocol, build_runtime_request
from runtime.runtime_execution_trace import record_execution
from runtime.execution_aiwitness_bridge import project_execution_to_aiwitness
from runtime.aiwitness_observation_bridge import return_witness_to_observation
from runtime.observation_evidence_candidate import build_evidence_candidate
from runtime.observation_evidence_validation import validate_evidence_candidate


def candidate():
    approved = HumanApprovedProtocol(
        "approval-01", "protocol-01", "human-01",
        ("bounded-action",), "candidate-01", "2026-09-28T00:00:00Z"
    )
    request = build_runtime_request(request_id="runtime-01", approved=approved)
    trace = record_execution(trace_id="trace-01", request=request, status="completed")
    witness = project_execution_to_aiwitness(witness_id="witness-01", trace=trace)
    observation = return_witness_to_observation(
        observation_id="observation-01", witness=witness
    )
    return build_evidence_candidate(
        candidate_id="evidence-candidate-01", observation=observation
    )


def test_pending_candidate_can_be_structurally_validated():
    validated = validate_evidence_candidate(candidate())

    assert validated.validation_status == "validated"
    assert validated.observation_id == "observation-01"
    assert validated.trace_id == "trace-01"
    assert validated.evidence_id is None
    assert validated.decision_authority is False


def test_validation_does_not_create_evidence_id():
    value = validate_evidence_candidate(candidate())
    assert value.evidence_id is None


def test_validation_rejects_non_pending_candidate():
    value = candidate()
    value = value.__class__(**{**value.__dict__, "validation_status": "validated"})
    try:
        validate_evidence_candidate(value)
    except ValueError as exc:
        assert "pending" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_validation_rejects_authority():
    value = candidate()
    value = value.__class__(**{**value.__dict__, "decision_authority": True})
    try:
        validate_evidence_candidate(value)
    except ValueError as exc:
        assert "decision_authority" in str(exc)
    else:
        raise AssertionError("expected ValueError")
