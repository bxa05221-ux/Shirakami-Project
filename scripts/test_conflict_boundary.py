from runtime.conflict_boundary import ConflictSignal, ConflictTrace, FuturePath


def test_conflict_preserves_act_and_stop_signals():
    trace = ConflictTrace()
    trace.record_signal(ConflictSignal("s1", "act", "動け、自分"))
    trace.record_signal(ConflictSignal("s2", "stop", "止まれ、自分"))

    assert trace.direction_weight("act") == 1.0
    assert trace.direction_weight("stop") == 1.0
    assert len(trace.signals()) == 2


def test_deadman_life_and_loss_paths_are_distinct():
    trace = ConflictTrace()
    trace.record_path(FuturePath("d1", "candidate path consequences", "deadman"))
    trace.record_path(FuturePath("l1", "alternative viable future", "life", ("life",)))
    trace.record_path(FuturePath("x1", "surrender some value while preserving life", "loss", ("life",)))

    assert len(trace.paths("deadman")) == 1
    assert len(trace.paths("life")) == 1
    assert len(trace.paths("loss")) == 1


def test_conflict_boundary_does_not_decide():
    trace = ConflictTrace()
    assert trace.human_gate_required is True
    assert trace.decision_authority is False
