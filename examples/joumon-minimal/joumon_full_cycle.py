"""Full JOUMON PoC cycle: Matome -> runtimes -> handoff -> verification -> Human Gate."""
from typing import Any, Mapping
from joumon_matome_loader import load_matome_mapping
from joumon_live_pipeline import run_live_observation
from joumon_semantic_handoff import create_handoff
from joumon_matome_yaml import handoff_to_matome_yaml, validate_matome_document
from joumon_handoff_import import matome_to_handoff
from joumon_evidence_verifier import verify
from joumon_human_gate import prepare_human_gate, record_human_decision


def run_full_cycle(document: Mapping[str, Any], providers, decision: str):
    context, protocol = load_matome_mapping(document)
    observations = tuple(
        run_live_observation(context=context, protocol=protocol, runtime_id=rid, provider=name, invoke=invoke)
        for rid, name, invoke in providers
    )
    evidence = tuple(e for e, _ in observations)
    lineage = tuple(l for _, l in observations)
    handoff = create_handoff(
        handoff_id="joumon-full-cycle-001",
        context_id=context.context_id,
        protocol_id=protocol.protocol_id,
        evidence=evidence,
        lineage=lineage,
    )
    artifact = handoff_to_matome_yaml(handoff)
    restored = matome_to_handoff(validate_matome_document(artifact))
    verification = tuple(
        verify(e, expected_context_id=context.context_id, expected_protocol_id=protocol.protocol_id)
        for e in restored.evidence
    )
    gate = prepare_human_gate(
        gate_id="joumon-full-cycle-gate",
        context_id=context.context_id,
        protocol_id=protocol.protocol_id,
        evidence=restored.evidence,
        verification_ids=tuple(v.evidence_id for v in verification),
    )
    decision_record = record_human_decision(gate, decision=decision)
    return {
        "context": context,
        "protocol": protocol,
        "handoff": restored,
        "verification": verification,
        "human_gate": decision_record,
        "artifact": artifact,
    }
