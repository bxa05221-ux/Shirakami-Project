from runtime.human_approved_runtime_request import HumanApprovedProtocol, build_runtime_request
from runtime.runtime_execution_trace import record_execution
from runtime.execution_aiwitness_bridge import project_execution_to_aiwitness
from runtime.aiwitness_observation_bridge import return_witness_to_observation
from runtime.observation_evidence_candidate import build_evidence_candidate


def test_observation_becomes_reviewable_candidate_not_evidence():
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
    candidate = build_evidence_candidate(
        candidate_id="evidence-candidate-01", observation=observation
    )

    assert candidate.observation_id == "observation-01"
    assert candidate.witness_id == "witness-01"
    assert candidate.validation_status == "pending"
    assert candidate.evidence_id is None
    assert candidate.decision_authority is False
