from runtime.reobservation_lineage import ReObservationLineage, ReObservationLink
from runtime.symbolic_reobservation import record_symbolic_reobservation
from runtime.symbolic_recursion import SymbolicRecursion, SymbolicTrace


def test_symbolic_trace_is_bound_to_reobservation_lineage():
    symbolic = SymbolicRecursion()
    lineage = ReObservationLineage()
    symbol = SymbolicTrace(
        symbol_id="symbol-home",
        expression="家",
        interpretations=("safety", "constraint", "belonging"),
        context_refs=("lived-01",),
    )
    link = ReObservationLink(
        link_id="link-symbolic-01",
        request_id="reobs-01",
        source_observation_id="obs-01",
        result_observation_id="obs-09",
        sequence=30,
    )

    record = record_symbolic_reobservation(
        symbolic=symbolic,
        lineage=lineage,
        symbol=symbol,
        link=link,
    )

    assert lineage.observations_for("reobs-01") == ("obs-09",)
    assert symbolic.traces()[0].symbol_id == "symbol-home"
    assert record.symbol_id == "symbol-home"
    assert record.interpretations == ("safety", "constraint", "belonging")


def test_symbolic_reobservation_keeps_interpretation_unresolved():
    symbolic = SymbolicRecursion()
    lineage = ReObservationLineage()
    symbol = SymbolicTrace(
        symbol_id="symbol-life",
        expression="生きる",
        interpretations=("survival", "continuation", "renewal"),
    )
    link = ReObservationLink("link-02", "reobs-02", "obs-02", "obs-10", 31)

    record = record_symbolic_reobservation(
        symbolic=symbolic,
        lineage=lineage,
        symbol=symbol,
        link=link,
    )

    assert len(record.interpretations) == 3
    assert record.human_gate_required is True
    assert record.decision_authority is False
