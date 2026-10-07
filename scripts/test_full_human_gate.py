import pytest
from runtime.full_human_gate import FullHumanGateError, validate_full_human_gate
from runtime.human_decision_signature import sign_human_decision
SECRET=b"test-secret"
D={"decision_id":"D1","approval_id":"A1","context_version":"C1","evidence_hash":"E1","protocol_hash":"P1","proposal_id":"PR1","principal_id":"H1","authentication_id":"AUTH1","key_id":"K1","decision":"approve","actor_type":"human","human_approval":True,"runtime_authority":False}
I={**{k:D[k] for k in ("decision_id","approval_id","context_version","evidence_hash","protocol_hash","proposal_id")},"principal_id":"H1","authentication_id":"AUTH1","actor_type":"human","authenticated":True,"authentication_method":"test"}
A={**D}
E={**D,"execution_id":"X1"}
UI={**{k:D[k] for k in ("decision_id","approval_id","context_version","evidence_hash","protocol_hash","proposal_id")},"event_type":"human_interaction","action":"approve","synthetic":False,"runtime_generated":False,"actor_type":"human","human_approval":True}
KW={"decision_time":"2026-10-07T10:00:00+00:00","trusted_principals":frozenset({"H1"}),"trusted_keys":frozenset({"K1"}),"trusted_from":"2026-10-01T00:00:00+00:00"}
def gate(d=D,p=A,i=I,e=E,u=UI,**extra):
    return validate_full_human_gate(ui_event=u,identity=i,decision=d,approval=p,execution=e,signature=sign_human_decision(d,SECRET),secret=SECRET,persisted=p,**KW,**extra)
def test_valid_full_chain_passes(): gate()
@pytest.mark.parametrize("field",["context_version","evidence_hash","protocol_hash","proposal_id","approval_id"])
def test_execution_binding_mutation_blocks(field):
    with pytest.raises(FullHumanGateError): gate(e={**E,field:"MUTATED"})
def test_synthetic_ui_blocks():
    with pytest.raises(FullHumanGateError): gate(u={**UI,"synthetic":True})
def test_runtime_generated_ui_blocks():
    with pytest.raises(FullHumanGateError): gate(u={**UI,"runtime_generated":True})
def test_decision_replay_blocks():
    with pytest.raises(FullHumanGateError): gate(seen_decision_ids=frozenset({"D1"}))
def test_ui_decision_binding_mutation_blocks():
    with pytest.raises(FullHumanGateError): gate(u={**UI,"evidence_hash":"E2"})
def test_runtime_actor_spoof_blocks():
    with pytest.raises(FullHumanGateError): gate(d={**D,"actor_type":"runtime"},u={**UI,"actor_type":"runtime"})
def test_authentication_replay_blocks():
    with pytest.raises(FullHumanGateError): gate(seen_authentication_ids=frozenset({"AUTH1"}))
def test_key_rotation_blocks():
    with pytest.raises(FullHumanGateError): gate(current_revoked_keys=frozenset({"K1"}))
def test_persisted_cross_context_substitution_blocks():
    with pytest.raises(FullHumanGateError): gate(p={**A,"context_version":"C2"})
def test_runtime_authority_claim_blocks():
    d={**D,"runtime_authority":True}
    with pytest.raises(FullHumanGateError): gate(d=d,p={**A,"runtime_authority":True},u={**UI,"actor_type":"human"})
def test_stale_key_blocks():
    with pytest.raises(FullHumanGateError): gate(decision_time="2026-09-01T10:00:00+00:00")
def test_human_identity_substitution_blocks():
    with pytest.raises(FullHumanGateError): gate(d={**D,"principal_id":"H2"})
def test_full_chain_still_requires_human_approval():
    with pytest.raises(FullHumanGateError): gate(d={**D,"human_approval":False},u={**UI,"human_approval":False})
