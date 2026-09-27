from runtime.symbolic_context_bridge import build_symbolic_context_transition
from runtime.symbolic_recursion import SymbolicRecursion, SymbolicTrace


def test_symbolic_interpretation_is_preserved_in_transition_provenance():
    boundary = SymbolicRecursion()
    symbol = SymbolicTrace(
        symbol_id="symbol-parent",
        expression="親",
        interpretations=("care", "control", "absence"),
        context_refs=("lived-01",),
    )

    transition = build_symbolic_context_transition(
        symbolic=boundary,
        symbol=symbol,
        observation={
            "observation_id": "obs-01",
            "unresolved_items": ("meaning-01",),
        },
        transition_id="ct-01",
        sequence=1,
        from_context_id="ctx-01",
        to_context_id="ctx-02",
    )

    assert transition.observation_id == "obs-01"
    assert transition.unresolved_items == ("meaning-01",)
    assert transition.provenance["symbolic_recursion"]["symbol_id"] == "symbol-parent"
    assert transition.provenance["symbolic_recursion"]["interpretations"] == [
        "care",
        "control",
        "absence",
    ]
    assert transition.human_gate_required is True
    assert transition.decision_authority is False


def test_symbolic_bridge_does_not_select_one_interpretation():
    boundary = SymbolicRecursion()
    symbol = SymbolicTrace(
        symbol_id="symbol-god",
        expression="神",
        interpretations=("rescue", "judgment", "hope"),
    )

    transition = build_symbolic_context_transition(
        symbolic=boundary,
        symbol=symbol,
        observation={"observation_id": "obs-02"},
        transition_id="ct-02",
        sequence=1,
        from_context_id="ctx-a",
        to_context_id="ctx-b",
    )

    assert len(
        transition.provenance["symbolic_recursion"]["interpretations"]
    ) == 3
