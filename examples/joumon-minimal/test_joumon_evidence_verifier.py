from joumon_provider_contract_poc import run
from joumon_evidence_adapter import to_evidence
from joumon_evidence_verifier import verify

def records():
    c,p,results=run()
    return c,p,[to_evidence(c.context_id,p.protocol_id,r.runtime_id,r.output,r.metadata) for r in results]

def test_valid_evidence_verifies():
    c,p,rs=records()
    out=verify(rs[0],expected_context_id=c.context_id,expected_protocol_id=p.protocol_id)
    assert out.verified is True
    assert "context_identity" in out.checks
    assert "protocol_identity" in out.checks
    assert "runtime_provenance" in out.checks

def test_wrong_context_fails_verification():
    c,p,rs=records()
    out=verify(rs[0],expected_context_id="wrong",expected_protocol_id=p.protocol_id)
    assert out.verified is False

def test_wrong_protocol_fails_verification():
    c,p,rs=records()
    out=verify(rs[0],expected_context_id=c.context_id,expected_protocol_id="wrong")
    assert out.verified is False

def test_verification_does_not_grant_authority():
    c,p,rs=records()
    out=verify(rs[0],expected_context_id=c.context_id,expected_protocol_id=p.protocol_id)
    assert out.verification_authority=="non-authoritative"
    assert out.final_decision_authority=="human"

def test_mock_execution_is_explicitly_verifiable_as_mock():
    _,_,rs=records()
    assert all(verify(r,expected_context_id=r.context_id,expected_protocol_id=r.protocol_id).verified for r in rs)
