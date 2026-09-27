from runtime.symbolic_recursion import SymbolicRecursion, SymbolicTrace


def test_symbolic_trace_preserves_multiple_interpretations():
    trace = SymbolicTrace(
        symbol_id="symbol-god",
        expression="神",
        interpretations=("救済", "権威", "不在", "希望"),
        context_refs=("family-01", "faith-01"),
    )

    boundary = SymbolicRecursion()
    boundary.record(trace)

    assert boundary.interpretations("symbol-god") == (
        "救済",
        "権威",
        "不在",
        "希望",
    )
    assert boundary.context_refs("symbol-god") == ("family-01", "faith-01")


def test_symbol_is_not_resolved_to_one_meaning():
    boundary = SymbolicRecursion()
    boundary.record(
        SymbolicTrace(
            symbol_id="symbol-parent",
            expression="親",
            interpretations=("protective", "controlling", "absent"),
        )
    )

    assert len(boundary.interpretations("symbol-parent")) == 3


def test_append_only_duplicate_symbol_is_rejected():
    boundary = SymbolicRecursion()
    boundary.record(SymbolicTrace(symbol_id="s1", expression="生きろ"))

    try:
        boundary.record(SymbolicTrace(symbol_id="s1", expression="生きろ"))
    except ValueError as exc:
        assert "duplicate symbol_id" in str(exc)
    else:
        raise AssertionError("duplicate symbol_id must be rejected")


def test_symbolic_recursion_returns_to_context_without_authority():
    boundary = SymbolicRecursion()

    assert boundary.returns_to_context is True
    assert boundary.decision_authority is False
    assert boundary.human_gate_required is True
