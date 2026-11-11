from runtime.context_transition import ContextTransition, ContextTransitionHistory


def test_observation_transition_preserves_unresolved_items():
    observation = {
        "observation_id": "obs-001",
        "unresolved_items": ["meaning-not-set", "missing-context"],
    }
    transition = ContextTransition.from_observation(
        observation,
        transition_id="ctx-001",
        sequence=1,
        from_context_id="ctx-before",
        to_context_id="ctx-after",
        transition_kind="candidate",
        provenance={"source": "observation:obs-001"},
    )

    assert transition.observation_id == "obs-001"
    assert transition.unresolved_items == (
        "meaning-not-set",
        "missing-context",
    )
    assert transition.transition_kind == "candidate"
    assert transition.human_gate_required is True
    assert transition.decision_authority is False


def test_history_is_append_only_and_monotonic():
    history = ContextTransitionHistory()
    history.append(
        ContextTransition(
            transition_id="ctx-001",
            sequence=1,
            observation_id="obs-001",
            from_context_id="ctx-0",
            to_context_id="ctx-1",
        )
    )
    history.append(
        ContextTransition(
            transition_id="ctx-002",
            sequence=2,
            observation_id="obs-002",
            from_context_id="ctx-1",
            to_context_id="ctx-2",
            unresolved_items=("still-open",),
        )
    )

    assert [item.transition_id for item in history.items()] == [
        "ctx-001",
        "ctx-002",
    ]
    assert history.unresolved_items() == ("still-open",)


def test_duplicate_or_non_monotonic_history_is_rejected():
    history = ContextTransitionHistory()
    first = ContextTransition(
        transition_id="ctx-001",
        sequence=1,
        observation_id="obs-001",
        from_context_id="ctx-0",
        to_context_id="ctx-1",
    )
    history.append(first)

    try:
        history.append(first)
        raise AssertionError("duplicate transition was accepted")
    except ValueError as exc:
        assert "duplicate transition_id" in str(exc)

    try:
        history.append(
            ContextTransition(
                transition_id="ctx-000",
                sequence=0,
                observation_id="obs-000",
                from_context_id="ctx-0",
                to_context_id="ctx-x",
            )
        )
        raise AssertionError("non-monotonic transition was accepted")
    except ValueError as exc:
        assert "monotonically" in str(exc)


def test_transition_does_not_grant_authority():
    transition = ContextTransition(
        transition_id="ctx-001",
        sequence=1,
        observation_id="obs-001",
        from_context_id="ctx-0",
        to_context_id="ctx-1",
    )
    payload = transition.to_dict()

    assert payload["human_gate_required"] is True
    assert payload["decision_authority"] is False
