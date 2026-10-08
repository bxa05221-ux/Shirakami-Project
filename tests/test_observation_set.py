from protocol.observation_set import build_observation_set


def test_observation_set_preserves_disagreement():
    observations = [
        {"observer_id": "a", "perspective": "structure", "observation": "same"},
        {"observer_id": "b", "perspective": "counterpoint", "observation": "different"},
    ]

    result = build_observation_set(observations)

    assert result["agreement"] == []
    assert len(result["differences"]) == 2
    assert result["differences"][0]["observation"] == "same"
    assert result["differences"][1]["observation"] == "different"
    assert result["decision_authority"] is False
    assert result["human_gate_required"] is True
