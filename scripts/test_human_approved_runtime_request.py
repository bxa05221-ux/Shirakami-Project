from runtime.human_approved_runtime_request import HumanApprovedProtocol, build_runtime_request


def test_runtime_request_requires_human_approved_protocol():
    approved = HumanApprovedProtocol(
        approval_id="approval-01",
        protocol_id="protocol-01",
        approver_id="human-01",
        scope=("bounded-action",),
        candidate_id="candidate-01",
        approved_at="2026-09-28T00:00:00Z",
    )

    request = build_runtime_request(request_id="runtime-01", approved=approved)

    assert request.human_approved is True
    assert request.decision_authority is False
    assert request.scope == ("bounded-action",)
    assert request.approval_id == "approval-01"


def test_empty_approval_scope_is_rejected():
    try:
        HumanApprovedProtocol(
            approval_id="approval-02",
            protocol_id="protocol-02",
            approver_id="human-01",
            scope=(),
            candidate_id="candidate-02",
            approved_at="2026-09-28T00:00:00Z",
        )
    except ValueError:
        return
    raise AssertionError("empty approval scope must be rejected")
