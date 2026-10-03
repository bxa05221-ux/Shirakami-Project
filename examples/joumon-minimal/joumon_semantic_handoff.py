"""Minimal semantic handoff preserving Context, Evidence and Lineage."""
from dataclasses import dataclass
from typing import Tuple
from joumon_evidence_adapter import UnifiedEvidence
from joumon_lineage import EvidenceLineage

@dataclass(frozen=True)
class SemanticHandoff:
    handoff_id: str
    context_id: str
    protocol_id: str
    evidence: Tuple[UnifiedEvidence, ...]
    lineage: Tuple[EvidenceLineage, ...]
    authority: str = "non-authoritative"
    final_decision_authority: str = "human"


def create_handoff(*, handoff_id: str, context_id: str, protocol_id: str,
                   evidence: Tuple[UnifiedEvidence, ...],
                   lineage: Tuple[EvidenceLineage, ...]) -> SemanticHandoff:
    if any(e.context_id != context_id or e.protocol_id != protocol_id for e in evidence):
        raise ValueError("Evidence does not match handoff Context/Protocol")
    if any(l.evidence_id not in {e.evidence_id for e in evidence} for l in lineage):
        raise ValueError("Lineage contains Evidence outside the handoff")
    return SemanticHandoff(handoff_id, context_id, protocol_id, evidence, lineage)
