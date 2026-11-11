import pytest
from runtime.human_decision_signature import sign_human_decision
from runtime.authenticated_human_gate import AuthenticatedHumanGateError, validate_authenticated_human_gate

SECRET=b"test-secret"
D={"decision_id":"D1","approval_id":"A1","context_version":"C1","evidence_hash":"E1","protocol_hash":"P1","proposal_id":"PR1","principal_id":"H1","authentication_id":"AUTH1","key_id":"K1","decision":"approve","actor_type":"human","human_approval":True,"runtime_authority":False}
A={**D}
I={**{k:D[k] for k in ("decision_id","approval_id","context_version","evidence_hash","protocol_hash","proposal_id")},"principal_id":"H1","authentication_id":"AUTH1","actor_type":"human","authenticated":True,"authentication_method":"test"}
KW={"decision_time":"2026-10-07T10:00:00+00:00","trusted_principals":frozenset({"H1"}),"trusted_keys":frozenset({"K1"}),"trusted_from":"2026-10-01T00:00:00+00:00"}
def validate(d=D,p=A,i=I,**extra):
    return validate_authenticated_human_gate(identity=i,decision=d,approval=p,signature=sign_human_decision(d,SECRET),secret=SECRET,persisted=p,**KW,**extra)
def test_full_chain_passes(): validate()
def test_revoked_key_blocks():
    with pytest.raises(AuthenticatedHumanGateError): validate(current_revoked_keys=frozenset({"K1"}))
def test_runtime_authority_blocks():
    d={**D,"runtime_authority":True}
    with pytest.raises(AuthenticatedHumanGateError): validate(d=d,p={**A,"runtime_authority":True})
def test_persisted_binding_mutation_blocks():
    with pytest.raises(AuthenticatedHumanGateError): validate(p={**A,"proposal_id":"PR2"})
