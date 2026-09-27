from runtime.reobservation_lineage import ReObservationLineage, ReObservationLink


def test_lineage_connects_unresolved_request_to_later_observation():
    lineage = ReObservationLineage()
    lineage.record(
        ReObservationLink(
            link_id="link-001",
            request_id="reobs-001",
            source_observation_id="obs-001",
            result_observation_id="obs-009",
            sequence=20,
        )
    )

    assert lineage.observations_for("reobs-001") == ("obs-009",)
    assert lineage.items()[0].source_observation_id == "obs-001"


def test_request_can_have_only_one_recorded_result():
    lineage = ReObservationLineage()
    first = ReObservationLink("link-001", "reobs-001", "obs-001", "obs-009", 20)
    lineage.record(first)

    try:
        lineage.record(
            ReObservationLink("link-002", "reobs-001", "obs-001", "obs-010", 21)
        )
        raise AssertionError("request received multiple lineage results")
    except ValueError as exc:
        assert "already linked" in str(exc)


def test_lineage_preserves_authority_boundary():
    lineage = ReObservationLineage()
    assert lineage.human_gate_required is True
    assert lineage.decision_authority is False
