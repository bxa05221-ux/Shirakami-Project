from runtime.symbolic_reobservation import SymbolicReObservationRecord


def test_symbolic_record_is_not_evidence():
    record = SymbolicReObservationRecord(
        link_id="link-01",
        request_id="reobs-01",
        source_observation_id="obs-01",
        result_observation_id="obs-02",
        symbol_id="symbol-god",
        expression="神",
        interpretations=("rescue", "authority", "hope"),
        context_refs=("ctx-01",),
    )

    assert not hasattr(record, "evidence_id")
    assert record.human_gate_required is True
    assert record.decision_authority is False


def test_multiple_interpretations_remain_distinct():
    record = SymbolicReObservationRecord(
        "link-02",
        "reobs-02",
        "obs-03",
        "obs-04",
        "symbol-parent",
        "親",
        ("care", "control", "absence"),
        (),
    )

    assert len(record.interpretations) == 3
    assert record.interpretations != ("care",)
