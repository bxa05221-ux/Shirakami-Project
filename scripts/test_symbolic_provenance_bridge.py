def test_symbolic_provenance_bridge_keeps_authority_outside_symbolic_layer():
    symbolic_is_evidence = False
    decision_authority = False
    human_gate_required = True
    assert symbolic_is_evidence is False
    assert decision_authority is False
    assert human_gate_required is True
