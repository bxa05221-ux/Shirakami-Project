from runtime.symbolic_decision_boundary import build_symbolic_decision_boundary


def test_symbolic_candidate_requires_human_gate():
    boundary = build_symbolic_decision_boundary(
        candidate_id="candidate-01",
        symbol_id="symbol-life",
        expression="生きろ",
        interpretations=("survival", "renewal", "continuation"),
        basis_observation_ids=("obs-10",),
    )

    request = boundary.as_human_gate_request()
    assert request["human_gate_required"] is True
    assert request["decision_authority"] is False
    assert request["basis_observation_ids"] == ["obs-10"]


def test_symbolic_candidate_does_not_select_one_interpretation():
    boundary = build_symbolic_decision_boundary(
        candidate_id="candidate-02",
        symbol_id="symbol-parent",
        expression="親",
        interpretations=("care", "control", "absence"),
        basis_observation_ids=("obs-11", "obs-12"),
    )

    assert boundary.candidate.interpretations == ("care", "control", "absence")


def test_symbolic_candidate_requires_observation_provenance():
    try:
        build_symbolic_decision_boundary(
            candidate_id="candidate-03",
            symbol_id="symbol-god",
            expression="神",
            interpretations=("hope",),
            basis_observation_ids=(),
        )
    except ValueError as exc:
        assert "observation provenance" in str(exc)
    else:
        raise AssertionError("symbolic candidate must retain observation provenance")
