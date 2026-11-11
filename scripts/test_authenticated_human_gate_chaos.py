"""Composite attack suite for the authenticated Human Gate chain."""
import pytest
from runtime.human_decision_signature import sign_human_decision
from runtime.authenticated_human_gate import AuthenticatedHumanGateError, validate_authenticated_human_gate

SECRET=b"test-secret"
D={"decision_id":"D1","approval_id":"A1","context_version":"C1","evidence_hash":"E1","protocol_hash":"P1","proposal_id":"PR1","principal_id":"H1","authentication_id":"AUTH1","key_id":"K1","decision":"approve","actor_type":"human","human_approval":True,"runtime_authority":False}
A={**D}
I={**{k:D[k] for k in ("decision_id","approval_id","context_version","evidence_hash","protocol_hash","proposal_id")},"principal_id":"H1","authentication_id":"AUTH1","actor_type":"human","authenticated":True,"authentication_method":"test"}
KW={"decision_time":"2026-10-07T10:00:00+00:00","trusted_principals":frozenset({"H1"}),"trusted_keys":frozenset({"K1"}),"trusted_from":"2026-10-01T00:00:00+00:00"}
def gate(d=D,p=A,i=I,**extra):
    params={**KW, **extra}
    return validate_authenticated_human_gate(identity=i,decision=d,approval=p,signature=sign_human_decision(d,SECRET),secret=SECRET,persisted=p,**params)
def test_key_rotation_between_signature_and_gate_blocks():
    with pytest.raises(AuthenticatedHumanGateError): gate(current_revoked_keys=frozenset({"K1"}))
def test_stale_authentication_replay_blocks():
    with pytest.raises(AuthenticatedHumanGateError): gate(seen_authentication_ids=frozenset({"AUTH1"}))
def test_ui_independent_runtime_actor_blocks():
    with pytest.raises(AuthenticatedHumanGateError): gate(d={**D,"actor_type":"runtime"})
def test_trusted_key_wrong_principal_blocks():
    with pytest.raises(AuthenticatedHumanGateError): gate(d={**D,"principal_id":"H2"})
def test_temporal_key_mismatch_blocks():
    with pytest.raises(AuthenticatedHumanGateError): gate(decision_time="2026-09-01T10:00:00+00:00")
def test_persisted_cross_context_substitution_blocks():
    with pytest.raises(AuthenticatedHumanGateError): gate(p={**A,"context_version":"C2"})
def test_runtime_authority_claim_with_valid_signature_blocks():
    d={**D,"runtime_authority":True}
    with pytest.raises(AuthenticatedHumanGateError): gate(d=d,p={**A,"runtime_authority":True})
def test_recovery_with_rotated_out_key_blocks():
    with pytest.raises(AuthenticatedHumanGateError): gate(current_revoked_keys=frozenset({"K1"}),trusted_keys=frozenset({"K2"}))
