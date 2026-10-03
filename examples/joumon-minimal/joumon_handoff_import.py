"""Reconstruct a JOUMON Semantic Handoff from a Matome-shaped document."""
from typing import Any
from joumon_evidence_adapter import UnifiedEvidence
from joumon_lineage import EvidenceLineage, LineageNode, LineageEdge
from joumon_semantic_handoff import SemanticHandoff


def matome_to_handoff(payload: dict[str, Any]) -> SemanticHandoff:
    authority = payload.get("authority", {})
    if authority.get("final_decision") != "human":
        raise ValueError("Matome document does not preserve human final authority")

    evidence = tuple(UnifiedEvidence(**item) for item in payload.get("evidence", []))
    evidence_ids = {e.evidence_id for e in evidence}
    lineage = []
    for item in payload.get("lineage", []):
        nodes = tuple(LineageNode(**n) for n in item.get("nodes", []))
        edges = tuple(LineageEdge(**e) for e in item.get("edges", []))
        record = EvidenceLineage(item["evidence_id"], nodes, edges, item.get("authority", "non-authoritative"))
        if record.evidence_id not in evidence_ids:
            raise ValueError("Lineage references Evidence outside the handoff")
        lineage.append(record)

    return SemanticHandoff(
        handoff_id=payload["handoff_id"],
        context_id=payload["context_id"],
        protocol_id=payload["protocol_id"],
        evidence=evidence,
        lineage=tuple(lineage),
        authority=authority.get("handoff", "non-authoritative"),
        final_decision_authority=authority["final_decision"],
    )
