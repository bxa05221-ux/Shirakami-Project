import yaml


def test_symbolic_human_gate_contract():
    with open("api/SYMBOLIC_HUMAN_GATE_CONTRACT.yaml", encoding="utf-8") as f:
        contract = yaml.safe_load(f)["symbolic_human_gate"]

    assert contract["candidate"]["decision_authority"] is False
    assert contract["candidate"]["human_gate_required"] is True
    assert contract["provenance"]["observation_ids_required"] is True
    assert contract["interpretation"]["plural"] is True
    assert contract["interpretation"]["authoritative"] is False
    assert contract["evidence"]["creates_evidence_id"] is False
    assert contract["execution"]["requires_human_gate"] is True
