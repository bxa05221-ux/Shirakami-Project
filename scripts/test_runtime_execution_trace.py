from runtime.human_approved_runtime_request import HumanApprovedProtocol, build_runtime_request
from runtime.runtime_execution_trace import record_execution


def test_runtime_execution_trace_preserves_human_approval_lineage():
    approved = HumanApprovedProtocol(
        "approval-01", "protocol-01", "human-01", ("bounded-action",), "candidate-01", "2026-09-28T00:00:00Z"
    )
    request = build_runtime_request(request_id="runtime-01", approved=approved)
    trace = record_execution(trace_id="trace-01", request=request, status="completed")

    assert trace.approval_id == "approval-01"
    assert trace.protocol_id == "protocol-01"
    assert trace.request_id == "runtime-01"
    assert trace.scope == ("bounded-action",)
    assert trace.decision_authority is False


def test_unapproved_runtime_request_cannot_be_executed():
    approved = HumanApprovedProtocol(
        "approval-02", "protocol-02", "human-01", ("bounded-action",), "candidate-02", "2026-09-28T00:00:00Z"
    )
    request = build_runtime_request(request_id="runtime-02", approved=approved)
    request = request.__class__(**{**request.__dict__, "human_approved": False})

    try:
        record_execution(trace_id="trace-02", request=request, status="completed")
    except ValueError:
        return
    raise AssertionError("unapproved RuntimeRequest must not execute")
