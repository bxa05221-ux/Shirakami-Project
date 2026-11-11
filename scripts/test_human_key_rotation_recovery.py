import pytest
from runtime.human_key_rotation_recovery import HumanKeyRotationError, validate_key_rotation_recovery

D={"decision_id":"D1","approval_id":"A1","context_version":"C1","evidence_hash":"E1","protocol_hash":"P1","proposal_id":"PR1","principal_id":"H1","authentication_id":"AUTH1","key_id":"K1","human_approval":True,"runtime_authority":False}
S={**D}

def test_valid_recovery():
    validate_key_rotation_recovery(D,S,trusted_keys=frozenset({"K1"}))

def test_revoked_key_blocks_recovery():
    with pytest.raises(HumanKeyRotationError):
        validate_key_rotation_recovery(D,S,current_revoked_keys=frozenset({"K1"}),trusted_keys=frozenset({"K1"}))

def test_rotated_out_key_blocks_recovery():
    with pytest.raises(HumanKeyRotationError):
        validate_key_rotation_recovery(D,S,current_revoked_keys=frozenset({"K1"}),trusted_keys=frozenset({"K2"}))

def test_persisted_binding_mutation_blocks():
    with pytest.raises(HumanKeyRotationError):
        validate_key_rotation_recovery(D,{**S,"key_id":"K2"},trusted_keys=frozenset({"K1","K2"}))

def test_replay_scope_mutation_blocks():
    with pytest.raises(HumanKeyRotationError):
        validate_key_rotation_recovery(D,{**S,"approval_id":"A2"},trusted_keys=frozenset({"K1"}))

def test_runtime_authority_blocks():
    with pytest.raises(HumanKeyRotationError):
        validate_key_rotation_recovery(D,{**S,"runtime_authority":True},trusted_keys=frozenset({"K1"}))
