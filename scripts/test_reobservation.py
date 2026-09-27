from runtime.reobservation import ReObservationQueue


def test_unresolved_items_become_reobservation_requests():
    queue = ReObservationQueue()
    queue.enqueue(
        request_id="reobs-001",
        source_observation_id="obs-001",
        unresolved_items=("meaning-not-set", "missing-context"),
        context_id="ctx-2",
        sequence=10,
    )

    assert [item.unresolved_item for item in queue.pending()] == [
        "meaning-not-set",
        "missing-context",
    ]
    assert queue.human_gate_required is True
    assert queue.decision_authority is False


def test_reobservation_can_be_marked_observed_without_resolving_meaning():
    queue = ReObservationQueue()
    queue.enqueue(
        request_id="reobs-001",
        source_observation_id="obs-001",
        unresolved_items=("meaning-not-set",),
        context_id="ctx-2",
        sequence=10,
    )

    item = queue.mark_observed("reobs-001")

    assert item.status == "observed"
    assert item.unresolved_item == "meaning-not-set"
    assert queue.pending() == ()


def test_queue_rejects_duplicates_and_empty_requests():
    queue = ReObservationQueue()

    try:
        queue.enqueue(
            request_id="reobs-001",
            source_observation_id="obs-001",
            unresolved_items=(),
            context_id="ctx-2",
            sequence=10,
        )
        raise AssertionError("empty unresolved request was accepted")
    except ValueError as exc:
        assert "at least one" in str(exc)

    queue.enqueue(
        request_id="reobs-001",
        source_observation_id="obs-001",
        unresolved_items=("open-item",),
        context_id="ctx-2",
        sequence=10,
    )
    try:
        queue.enqueue(
            request_id="reobs-001",
            source_observation_id="obs-002",
            unresolved_items=("other-item",),
            context_id="ctx-3",
            sequence=20,
        )
        raise AssertionError("duplicate request was accepted")
    except ValueError as exc:
        assert "duplicate request_id" in str(exc)
