from runtime.symbolic_evidence_provenance import project_symbolic_provenance
from runtime.symbolic_reobservation import SymbolicReObservationRecord


def test_symbolic_origin_is_provenance_not_evidence():
    record = SymbolicReObservationRecord(
        link_id="link-01",
        request_id="reobs-01",
        source_observation_id="obs-01",
        result_observation_id="obs-02",
        symbol_id="symbol-parent",
        expression="親",
        interpretations=("care", "control", "absence"),
        context_refs=("ctx-01",),
    )

    provenance = project_symbolic_provenance(
        record,
        observation_id="obs-02",
        evidence_id="ev-02",
    )

    assert provenance["observation_id"] == "obs-02"
    assert provenance["evidence_id"] == "ev-02"
    assert provenance["symbolic_is_evidence"] is False
    assert provenance["decision_authority"] is False
    assert provenance["human_gate_required"] is True
    assert provenance["symbolic_origin"]["interpretations"] == [
        "care",
        "control",
        "absence",
    ]
