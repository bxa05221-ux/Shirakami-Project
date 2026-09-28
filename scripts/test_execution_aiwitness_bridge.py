from runtime.human_approved_runtime_request import HumanApprovedProtocol, build_runtime_request
from runtime.runtime_execution_trace import record_execution
from runtime.execution_aiwitness_bridge import project_execution_to_aiwitness


def test_execution_facts_reach_aiwitness_with_approval_lineage():
    approved = HumanApprovedProtocol(
        "approval-01", "protocol-01", "human-01",
        ("bounded-action",), "candidate-01", "2026-09-28T00:00:00Z"
    )
    request = build_runtime_request(request_id="runtime-01", approved=approved)
    trace = record_execution(trace_id="trace-01", request=request, status="completed")
    witness = project_execution_to_aiwitness(witness_id="witness-01", trace=trace)

    assert witness.trace_id == "trace-01"
    assert witness.approval_id == "approval-01"
    assert witness.protocol_id == "protocol-01"
    assert witness.request_id == "runtime-01"
    assert witness.execution_status == "completed"
    assert witness.decision_authority is False
