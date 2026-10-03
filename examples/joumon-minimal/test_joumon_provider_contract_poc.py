from joumon_provider_contract_poc import run

def test_provider_contract_preserves_context():
    context, protocol, results = run()
    assert protocol.input_context_id == context.context_id
    assert {r.context_id for r in results} == {context.context_id}

def test_multiple_provider_types_share_one_contract():
    _, _, results = run()
    assert {r.runtime_id for r in results} == {"openai-compatible", "gemini-compatible"}

def test_provider_identity_is_metadata_not_authority():
    context, _, results = run()
    assert context.final_decision_authority == "human"
    assert all(r.metadata["provider"] in {"openai", "gemini"} for r in results)

def test_provider_outputs_are_not_authoritative():
    _, _, results = run()
    assert all("requires human review" in r.output for r in results)

def test_provider_specific_details_stay_outside_context():
    context, _, _ = run()
    assert "provider" not in context.__dataclass_fields__
